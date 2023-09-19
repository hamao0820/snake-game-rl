import Countdown from './countdown';
import Food from './food';
import Judger from './judger';
import Score from './score';
import Snake from './snake';
import Stage from './stage';

class Model {
    readonly #snake: Snake;
    readonly #stage: Stage;
    #food: Food | null = null;
    #gameOver = false;
    #turnAngle = 0;
    #countdown: Countdown;
    constructor() {
        this.#snake = new Snake();
        this.#stage = new Stage();

        this.#food = this.createFood();
        this.#countdown = new Countdown();
    }

    update(ctx: CanvasRenderingContext2D) {
        this.#snake.turn(this.#turnAngle);
        this.#snake.move();

        if (this.#food && Judger.checkCollisionFood(this.#snake, this.#food)) {
            this.#food = this.createFood();
            this.#snake.grow();
            Score.addScore();
            return;
        }
        if (Judger.checkCollisionWall(this.#snake) || Judger.checkCollisionSelf(this.#snake, ctx)) {
            this.#gameOver = true;
        }
    }

    createFood() {
        const x = Math.random() * (Stage.Size - 2 * Snake.halfWidth) + Snake.halfWidth;
        const y = Math.random() * (Stage.Size - 2 * Snake.halfWidth) + Snake.halfWidth;
        return new Food(x, y);
    }

    set turnAngle(turnAngle: number) {
        this.#turnAngle = turnAngle;
    }

    get snake() {
        return this.#snake;
    }

    get stage() {
        return this.#stage;
    }

    get food() {
        return this.#food;
    }

    get gameOver() {
        return this.#gameOver;
    }

    get countdown() {
        return this.#countdown;
    }
}

export default Model;
