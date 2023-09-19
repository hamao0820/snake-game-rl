class Score {
    static #score: number = 0;
    static #element: HTMLDivElement;

    static init() {
        this.#score = 0;
        this.#element = document.getElementById('score') as HTMLDivElement;
        this.#element.innerHTML = `Score: ${this.#score.toString()}`;
    }

    static addScore() {
        this.#score += 10;
        this.#element.innerText = `Score: ${this.#score.toString()}`;
    }
}

export default Score;
