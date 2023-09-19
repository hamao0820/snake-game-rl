class Countdown {
    #time: number | null;
    #rapTime: number;

    constructor() {
        this.#time = null;
        this.#rapTime = Date.now();
    }

    // 時間を進める
    tick() {
        if (this.#time === null) throw new Error('time does not set');
        this.#time -= Date.now() - this.#rapTime;
        this.#rapTime = Date.now();
    }

    // 時間を設定する
    set time(time: number) {
        this.#rapTime = Date.now();
        this.#time = time;
    }

    get countDown() {
        if (this.#time === null) throw new Error('time does not set');
        return Math.ceil(this.#time / 1000);
    }
}

export default Countdown;
