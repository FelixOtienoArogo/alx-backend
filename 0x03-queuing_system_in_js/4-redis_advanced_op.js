import { createClient } from 'redis';
import redis from 'redis';

const client = createClient({
 host: 'localhost',
 port: 6379
});

client.on('connect', () => {
 console.log('Redis client connected to the server');
});

client.on('error', err => console.log('Redis client not connected to the server: ', err));

const keys = ['Portland', 'Seattle', 'New York', 'Bogota', 'Cali', 'Paris'];
const values = [50, 80, 20, 20, 40, 2];

keys.forEach((key, index) => client.hset('HolbertonSchools', key, values[index], redis.print));

client.hgetall('HolbertonSchools', (error, value) => console.log(value));
