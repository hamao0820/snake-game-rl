/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

import puppeteer, { Browser, ElementHandle, Page } from 'puppeteer';
import path from 'path';
import Model from '../snake-game/ts/model';
import Controller from '../snake-game/ts/controller';

declare const view: {
  ctx: CanvasRenderingContext2D;
  render: (
    positionList: [number, number][],
    gameOver: boolean,
    food: { x: number; y: number } | null,
    mx: number,
    my: number,
    angle: number
  ) => void;
};

declare const scoreRenderer: {
  render: (score: number) => void;
};

export type Action = 0 | 1 | 2;

class Simulator {
  #browser: Browser | null = null;
  #page: Page | null = null;
  #model: Model;
  #Controller: Controller;
  #canvas: ElementHandle<HTMLCanvasElement> | null = null;
  #prevScore = 0;
  #frameSkip = 3;
  constructor(frameSkip: number) {
    this.#model = new Model();
    this.#Controller = new Controller(this.#model);
    this.#frameSkip = frameSkip;
  }

  async init(headless: boolean | 'new' = 'new') {
    this.#browser = await puppeteer.launch({ headless });
    this.#page = await this.#browser.newPage();

    await this.#page.goto(`file://${path.resolve(__dirname, '..', 'snake-game', 'index.html')}`, {
      waitUntil: 'domcontentloaded',
    });

    this.#canvas = await this.#page.$('canvas');
    if (!this.#canvas) {
      throw new Error('canvas not found');
    }

    await this.step();
  }

  async step(action: Action = 0) {
    if (!this.#page) {
      throw new Error('initialize first.');
    }
    await new Promise((r) => setTimeout(r, 10 * this.#frameSkip));
    const isCollisionSelf = (await this.#page.evaluate<
      [
        positionList: [number, number][],
        gameOver: boolean,
        food: { x: number; y: number } | null,
        mx: number,
        my: number,
        angle: number,
        score: number
      ]
    >(
      (
        positionList: [number, number][],
        gameOver: boolean,
        food: { x: number; y: number } | null,
        mx: number,
        my: number,
        angle: number,
        score: number
      ) => {
        view.render(positionList, gameOver, food, mx, my, angle);
        scoreRenderer.render(score);
        const tx = mx + Math.cos((angle * Math.PI) / 180) * (8 + 2);
        const ty = my + Math.sin((angle * Math.PI) / 180) * (8 + 2);
        const index = (Math.trunc(ty) * 300 + Math.trunc(tx)) * 4;
        const data = view.ctx.getImageData(0, 0, 300, 300).data;
        return data[index] !== 0 || data[index + 1] !== 0 || data[index + 2] !== 0;
      },
      this.#model.snake.positionList,
      this.#model.gameOver,
      this.#model.food,
      this.#model.snake.mx,
      this.#model.snake.my,
      this.#model.snake.angle,
      this.#model.score
    )) as boolean;

    switch (action) {
      case 0:
        this.#Controller.stopTurn();
        break;
      case 1:
        this.#Controller.turnRight();
        break;
      case 2:
        this.#Controller.turnLeft();
        break;

      default: {
        return;
      }
    }

    for (let i = 0; i < this.#frameSkip; i++) this.#model.update(isCollisionSelf);

    const getReward = this.#prevScore !== this.#model.score;
    this.#prevScore = this.#model.score;

    return { done: this.#model.gameOver, score: this.#model.score, imageBuffer: await this.ss(), getReward };
  }

  async close() {
    if (this.#browser) {
      await this.#browser.close();
    }
    this.#browser = null;
    this.#page = null;

    return;
  }

  async ss(): Promise<Buffer> {
    if (!this.#canvas) {
      throw new Error('initialize first.');
    }
    const ss = (await this.#canvas.screenshot({ encoding: 'binary' })) as Buffer;
    return ss;
  }
}

export default Simulator;

// (async () => {
//   const simulator = new Simulator(3);
//   await simulator.init(false);
//   let action: Action = 0;
//   const readline = await import('readline');
//   while (!simulator.done) {
//     const rl = readline.createInterface({
//       input: process.stdin,
//       output: process.stdout,
//     });
//     const action = await new Promise<Action>((resolve) => {
//       rl.question('0: straight, 1: right, 2: left\naction: ', (action) => {
//         rl.close();
//         if (action === '0' || action === '1' || action === '2') {
//           resolve(Number(action) as Action);
//           return;
//         }
//         console.log('invalid action');
//         resolve(0);
//       });
//     });
//     await simulator.step(action);
//   }

//   await simulator.close();
// })();
