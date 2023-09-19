import Food from './food';
import Snake from './snake';
import Stage from './stage';

class Judger {
    static checkCollisionWall(snake: Snake) {
        return (
            snake.mx < Snake.halfWidth ||
            snake.mx >= Stage.Size - Snake.halfWidth ||
            snake.my < Snake.halfWidth ||
            snake.my >= Stage.Size - Snake.halfWidth
        );
    }

    static checkCollisionSelf(snake: Snake, ctx: CanvasRenderingContext2D) {
        const tx = snake.mx + Math.cos((snake.angle * Math.PI) / 180) * (Snake.halfWidth + 2);
        const ty = snake.my + Math.sin((snake.angle * Math.PI) / 180) * (Snake.halfWidth + 2);
        const data = ctx.getImageData(0, 0, Stage.Size, Stage.Size).data;
        const index = (Math.trunc(ty) * Stage.Size + Math.trunc(tx)) * 4;
        return data[index] !== 0 || data[index + 1] !== 0 || data[index + 2] !== 0;
    }

    static checkCollisionFood(snake: Snake, food: Food) {
        return (snake.mx - food.x) ** 2 + (snake.my - food.y) ** 2 <= ((Snake.halfWidth + 2) * 2) ** 2;
    }
}

export default Judger;
