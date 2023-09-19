import '../style.css';
import Game from './game';
import StartButton from './startButton';

class Main {
    constructor() {
        const game = new Game();
        game.init();

        StartButton.init(game);

        document.addEventListener(
            'dblclick',
            function (e) {
                e.preventDefault();
            },
            { passive: false }
        );
    }
}

document.addEventListener('DOMContentLoaded', () => new Main());
