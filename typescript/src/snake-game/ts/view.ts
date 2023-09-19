import Model from './model';
import Snake from './snake';
import Stage from './stage';

class View {
    readonly #model: Model;
    readonly #ctx: CanvasRenderingContext2D;
    constructor(model: Model) {
        this.#model = model;
        const canvas = document.getElementById('canvas') as HTMLCanvasElement;
        this.#ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
    }

    private renderStage() {
        this.#ctx.fillStyle = '#000';
        this.#ctx.fillRect(0, 0, Stage.Size, Stage.Size);
    }

    private renderSnake() {
        let i = 0;
        for (const [x, y] of this.#model.snake.positionList) {
            this.#ctx.fillStyle = this.#model.gameOver
                ? '#800'
                : `hsl(${120 - (this.#model.snake.positionList.length - i) * 2}deg, 100%, 50%)`;
            this.#ctx.beginPath();
            this.#ctx.arc(x, y, Snake.halfWidth, 0, 2 * Math.PI);
            this.#ctx.fill();
            this.#ctx.closePath();
            i++;
        }
    }

    private renderSnakeEye() {
        const lex =
            this.#model.snake.mx + Math.cos(((this.#model.snake.angle - 60) * Math.PI) / 180) * Snake.halfWidth * 0.4;
        const ley =
            this.#model.snake.my + Math.sin(((this.#model.snake.angle - 60) * Math.PI) / 180) * Snake.halfWidth * 0.4;
        const rex =
            this.#model.snake.mx + Math.cos(((this.#model.snake.angle + 60) * Math.PI) / 180) * Snake.halfWidth * 0.4;
        const rey =
            this.#model.snake.my + Math.sin(((this.#model.snake.angle + 60) * Math.PI) / 180) * Snake.halfWidth * 0.4;
        this.#ctx.fillStyle = '#fff';
        this.#ctx.beginPath();
        this.#ctx.arc(lex, ley, Snake.halfWidth * 0.4, 0, 2 * Math.PI);
        this.#ctx.fill();
        this.#ctx.closePath();
        this.#ctx.fillStyle = '#000';
        this.#ctx.beginPath();
        this.#ctx.arc(lex, ley, Snake.halfWidth * 0.2, 0, 2 * Math.PI);
        this.#ctx.fill();
        this.#ctx.closePath();

        this.#ctx.fillStyle = '#fff';
        this.#ctx.beginPath();
        this.#ctx.arc(rex, rey, Snake.halfWidth * 0.4, 0, 2 * Math.PI);
        this.#ctx.fill();
        this.#ctx.closePath();
        this.#ctx.fillStyle = '#000';
        this.#ctx.beginPath();
        this.#ctx.arc(rex, rey, Snake.halfWidth * 0.2, 0, 2 * Math.PI);
        this.#ctx.fill();
        this.#ctx.closePath();
    }

    private renderFood() {
        if (this.#model.food === null) {
            return;
        }
        this.#ctx.fillStyle = `hsl(${Math.random() * 360}, 100%, 50%)`;
        this.#ctx.beginPath();
        this.#ctx.arc(this.#model.food.x, this.#model.food.y, Snake.halfWidth, 0, 2 * Math.PI);
        this.#ctx.fill();
        this.#ctx.closePath();
    }

    renderCountdown() {
        this.#ctx.fillStyle = '#fff';
        this.#ctx.font = '15px';
        this.#ctx.textAlign = 'center';
        this.#ctx.textBaseline = 'middle';
        this.#ctx.fillText(
            this.#model.countdown.countDown.toString(),
            this.#model.snake.mx,
            this.#model.snake.my - Snake.halfWidth * 3
        );
    }

    render() {
        this.renderStage();
        this.renderSnake();
        this.renderSnakeEye();
        this.renderFood();
    }

    get ctx() {
        return this.#ctx;
    }
}

export default View;
