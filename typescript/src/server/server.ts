import Simulator, { Action } from '../simulater/simulator';

type Message = { method: 'reset'; data: {} } | { method: 'step'; data: { action: Action } };
type StepResponse = {
  observation: string | Buffer;
  reward: number;
  terminated: boolean;
  truncated: boolean;
  info: { [key: string]: string };
};
type ResetResponse = {
  state: string | Buffer;
  info: { [key: string]: string };
};

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
          await simulator.reset();
          const img = await simulator.ss();
          const res: ResetResponse = {
            state: img,
            info: {},
          };
          ws.send(JSON.stringify(res));
          return;
        }
        case 'step': {
          const action = Number(data.data.action) as Action;
          const state = await simulator.step(action);
          if (state === undefined) throw new Error('state is undefined');
          if (state.done) {
            const res: StepResponse = {
              observation: state.imageBuffer,
              reward: state.getReward ? 0 : -1,
              terminated: state.done,
              truncated: false,
              info: {},
            };
            ws.send(JSON.stringify(res));
            return;
          }
          const res: StepResponse = {
            observation: state.imageBuffer,
            reward: state.getReward ? 3 : 0.05,
            terminated: state.done,
            truncated: false,
            info: {},
          };
          ws.send(JSON.stringify(res));
          return;
        }
      }
    },
    open: (ws) => {
      ws.send('0: straight, 1: right, 2: left');
      console.log('open');
    },
    close: async (ws) => {
      console.log('close');
      ws.close();
      server.stop();
      await simulator.close();
    },
    drain: (ws) => {
      console.log('drain');
    },
  },
});

console.log(`Listening on localhost: ${server.port}`);
