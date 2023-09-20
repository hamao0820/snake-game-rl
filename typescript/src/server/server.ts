import Simulator, { Action } from '../simulater/simulator';

const simulator = new Simulator(3);
await simulator.init();

const server = Bun.serve<{ authToken: string }>({
  fetch(req, server) {
    const success = server.upgrade(req);
    if (success) {
      return undefined;
    }
    return new Response('Hello world!');
  },
  port: 8080,
  websocket: {
    message: async (ws, message) => {
      if (message === '0' || message === '1' || message === '2') {
        const action = Number(message) as Action;
        await simulator.step(action);
        const img = await simulator.ss();
        if (simulator.done) {
          ws.send(JSON.stringify({ done: true, img }));
          await simulator.close();
          ws.close();
          return;
        }
        ws.send(JSON.stringify({ done: false, img }));
        return;
      }
      ws.send('invalid action\n0: straight, 1: right, 2: left');
    },
    open: (ws) => {
      ws.send('0: straight, 1: right, 2: left');
      console.log('open');
    },
    close: (ws) => {
      console.log('close');
      server.stop();
    },
    drain: (ws) => {
      console.log('drain');
    },
  },
});

console.log(`Listening on localhost: ${server.port}`);
