class BoggleGame {
  constructor() {
    this.score = 0;
    this.timeRemaining = 60;
    this.form = $("form");
    this.timerDisplay = $("#timer-display");
    this.scoreDisplay = $("#score-display");
    this.submittedWords = new Set();

    this.form.on("submit", this.handleSubmit.bind(this));
    this.startCountdown();
  }

  handleSubmit(event) {
    event.preventDefault();
    const word = $('input[name="word"]').val().trim();

    if (word.length === 0 || this.submittedWords.has(word)) return;

    axios
      .post("/check-word", new FormData(this.form[0]))
      .then((response) => {
        const result = response.data.result;
        this.handleWordCheckResult(result, word);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  handleWordCheckResult(result, word) {
    let message = "";

    if (result === "ok") {
      message = "The word is valid and on the board!";
      this.score += word.length;
      this.scoreDisplay.text(`Score: ${this.score}`);
      this.submittedWords.add(word);
    } else if (result === "not-on-board") {
      message = "The word is valid but not on the board.";
    } else {
      message = "The word is not valid.";
    }

    alert(message);
  }

  startCountdown() {
    this.updateTimerDisplay();
    this.timerInterval = setInterval(() => {
      this.timeRemaining -= 1;
      this.updateTimerDisplay();

      if (this.timeRemaining <= 0) {
        clearInterval(this.timerInterval);
        this.endGame();
      }
    }, 1000);
  }

  updateTimerDisplay() {
    this.timerDisplay.text(`Time Remaining: ${this.timeRemaining}s`);
  }

  endGame() {
    clearInterval(this.timerInterval);
    this.form.off("submit");
    this.form.find("button[type='submit']").prop("disabled", true);

    axios
      .post("/update-stats", { score: this.score })
      .then((response) => {
        const highestScore = response.data.highest_score;
        const gamesPlayed = response.data.games_played;
        this.showStats(highestScore, gamesPlayed);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  showStats(highestScore, gamesPlayed) {
    alert(`Games played: ${gamesPlayed}\nHighest Score: ${highestScore}`);
  }
}

$(document).ready(function () {
  new BoggleGame();
});
