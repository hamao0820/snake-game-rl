import Model from './model';
import View from './view';

class Controller {
    readonly #view: View;
    readonly #model: Model;
    readonly #leftButton: HTMLButtonElement;
    readonly #rightButton: HTMLButtonElement;
    constructor(view: View, model: Model) {
        this.#view = view;
        this.#model = model;

        this.#leftButton = document.getElementById('left') as HTMLButtonElement;
        this.#rightButton = document.getElementById('right') as HTMLButtonElement;

        this.#leftButton.addEventListener('pointerdown', this.turnLeft.bind(this));
        this.#rightButton.addEventListener('pointerdown', this.turnRight.bind(this));
        this.#leftButton.addEventListener('pointerup', this.stopTurn.bind(this));
        this.#rightButton.addEventListener('pointerup', this.stopTurn.bind(this));
        document.addEventListener('keydown', (e: KeyboardEvent) => {
            if (e.key === 'ArrowLeft') {
                this.turnLeft(e);
            } else if (e.key === 'ArrowRight') {
                this.turnRight(e);
            }
        });
        document.addEventListener('keyup', (e: KeyboardEvent) => {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                this.stopTurn(e);
            }
        });
    }

    private turnLeft(e: MouseEvent | KeyboardEvent) {
        e.preventDefault();
        this.#model.turnAngle = -5;
    }

    private turnRight(e: MouseEvent | KeyboardEvent) {
        e.preventDefault();
        this.#model.turnAngle = 5;
    }

    private stopTurn(e: MouseEvent | KeyboardEvent) {
        e.preventDefault();
        this.#model.turnAngle = 0;
    }

    reset() {
        this.#leftButton.removeEventListener('pointerdown', this.turnLeft.bind(this));
        this.#rightButton.removeEventListener('pointerdown', this.turnRight.bind(this));
        this.#leftButton.removeEventListener('pointerup', this.stopTurn.bind(this));
        this.#rightButton.removeEventListener('pointerup', this.stopTurn.bind(this));
    }
}

export default Controller;
