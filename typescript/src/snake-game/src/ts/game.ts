import Controller from './controller';
import Model from './model';
import Score from './score';
import StartButton from './startButton';
import View from './view';

class Game {
    readonly #view: View;
    readonly #model: Model;

    constructor() {
        this.#model = new Model();
        this.#view = new View(this.#model);

        this.#view.render();
    }

    private step() {
        this.#model.update(this.#view.ctx);
        this.#view.render();
    }

    init() {
        Score.init();
    }

    async ready() {
        this.#model.countdown.time = 3000;
        while (this.#model.countdown.countDown > 0) {
            await new Promise((resolve) => setTimeout(resolve, 10));
            this.#model.countdown.tick();
            this.#view.render();
            this.#view.renderCountdown();
        }
        this.start();
    }

    async start() {
        const controller = new Controller(this.#view, this.#model);
        while (!this.#model.gameOver) {
            await new Promise((resolve) => setTimeout(resolve, 10));
            this.step();
        }
        controller.reset();
        StartButton.available();
    }
}

export default Game;
