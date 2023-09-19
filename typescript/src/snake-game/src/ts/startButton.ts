import Game from './game';

class StartButton {
    static #element: HTMLDivElement;

    static init(game: Game) {
        this.#element = document.getElementById('start') as HTMLDivElement;
        this.#element.onclick = () => this.start(game);
    }

    private static start(game: Game) {
        this.unavailable();
        this.#element.onclick = null;

        game.ready();
    }

    static restart() {
        this.unavailable();
        const game = new Game();
        game.init();
        this.start(game);
    }

    static unavailable() {
        this.#element.classList.add('unavailable');
    }

    static available() {
        this.#element.classList.remove('unavailable');
        this.#element.onclick = () => this.restart();
    }
}

export default StartButton;
