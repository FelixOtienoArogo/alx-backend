import redis from 'redis';
import { promisify } from 'util';
import express from 'express';
import { createQueue } from 'kue';

const client = redis.createClient();
const app = express();
const queue = createQueue();
const initSeats = 50;
const port = 1245;
let reservationEnabled = true;

async function reserveSeat(number){
	return promisify(client.SET).bind(client)('available_seats', number);
}

async function getCurrentAvailableSeats(){
	return promisify(client.GET).bind(client)('available_seats');
}

async function initialiseAvailableSeats(initialSeatsCount){
	return promisify(client.SET).bind(client)('available_seats', Number.parseInt(initialSeatsCount));
}

app.get('/available_seats', (_, res) => {
	getCurrentAvailableSeats().
		then((numberOfAvailableSeats) => {
			res.json({ numberOfAvailableSeats })
		});
});

app.get('/reserve_seat', (_, res) => {
	if(!reservationEnabled) {
		res.json({ status: 'Reservation are blocked'});
		return;
	}
	try{
	const job = queue.create('reserve_seat');
	job.save();
	res.json({ "status": "Reservation in process" });
	job.on('complete', () => {
		console.log(`Seat reservation job ${job.id} completed`);
	});
	job.on('failed', (err) => {
                console.log(`Seat reservation job ${job.id} failed: ${err.message || err.toString()}`);
        });
	} catch {
		res.json({ status: 'Reservation failed'});
	}
});

app.get('/process', (_req, res) => {
	res.json({ status: 'Queue processing' });
	queue.process('reserve_seat', (_job, done) => {
		getCurrentAvailableSeats().
			then((result) => Number.parseInt(result || 0)).
			then((availableSeats) => {
				if(availableSeats >= 1){
					reserveSeat(availableSeats - 1).
						then(() => done());
				} else {
					done(new Error('Not enough seats available'));
				}
			});
	});
});

app.listen(port, () => {
	initialiseAvailableSeats(process.env.initSeats || initSeats).
		then(() => {
			reservationEnabled = true;
		});
});
