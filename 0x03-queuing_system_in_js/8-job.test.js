const kue = require('kue');
const queue = kue.createQueue();
import createPushNotificationsJobs from './8-job.js';
const chai = require('chai');
const spies = require('chai-spies');
const expect = chai.expect;

chai.use(spies);

describe('createPushNotificationsJobs', () => {
 const logSpy = chai.spy.on(console, 'log');
 before(() => {
  queue.testMode.enter(true);
 });
  after(() => {
   queue.testMode.clear();
   queue.testMode.exit();
  });
  afterEach(() => logSpy.__spy.calls = []);
 const jobs = [
   {
     phoneNumber: '4153518780',
     message: 'This is the code 1234 to verify your account'
   },
   {
     phoneNumber: '4153518781',
     message: 'This is the code 4562 to verify your account'
   }
 ];
 it('display a error message if jobs is not an array', () => {
  expect(() => createPushNotificationsJobs(4, queue)).to.throw('Jobs is not an array');
 });
 it('create two new jobs to the queue', (done) => {
  expect(queue.testMode.jobs.length).to.equal(0);
  createPushNotificationsJobs(jobs, queue);
  expect(queue.testMode.jobs.length).to.equal(2);
  expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
  expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
  console.log(queue.testMode.jobs[0].id);
  queue.process('push_notification_code_3', () => {
  expect(logSpy).to.have.been.called.with(`Notification job created: ${queue.testMode.jobs[0].id}`);
  done();
  });
  });

 it('test that the jobs are completed', (done) => {
  queue.testMode.jobs[0].addListener('complete', () => {
   expect(logSpy).to.have.been.called.with(`Notification job ${queue.testMode.jobs[0].id} completed`);
   done();
  });
  queue.testMode.jobs[0].emit('complete');
 });

 it('test when job has failed', (done) => {
  queue.testMode.jobs[0].addListener('failed', () => {
   expect(logSpy).to.have.been.called.with(`Notification job ${queue.testMode.jobs[0].id} failed: Error: Failed to send`);
   done();
  });
  queue.testMode.jobs[0].emit('failed', new Error('Failed to send'));
 });

 it('test that job is making progress', (done) => {
  queue.testMode.jobs[0].addListener('progress', () => {
   expect(logSpy).to.have.been.called.with(`Notification job ${queue.testMode.jobs[0].id} 25% complete`);
   done();
  });
  queue.testMode.jobs[0].emit('progress', 25);
 });
});
