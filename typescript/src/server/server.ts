import Simulator, { Action } from '../simulater/simulator';

type Message = { method: 'reset'; data: {} } | { method: 'step'; data: { action: Action } };

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
      const data = JSON.parse(String(message)) as Message;
      switch (data.method) {
        case 'reset': {
          const img = await simulator.ss();
          ws.send(JSON.stringify({ img }));
          return;
        }
        case 'step': {
          const action = Number(data.data.action) as Action;
          const state = await simulator.step(action);
          if (state === undefined) return;
          if (state.done) {
            ws.send(JSON.stringify(state));
            await simulator.close();
            ws.close();
            return;
          }
          ws.send(JSON.stringify(state));
          return;
        }
      }
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
