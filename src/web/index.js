const app = Vue.createApp({
    data() {
        return {
            maxLetters: 10,
            loading: false,
            letters: "",
            language: "spanish",
            words: [],
            error: false,
            errorMessage: "",
            alertType: "alert-warning",
        }
    },
    methods: {
        checkKey(event) {
            if(event.key.length == 1 && event.key.toUpperCase() != event.key.toLowerCase() && this.letters.length < this.maxLetters)
                return true;
            else
                event.preventDefault();
        },
        showErrorMessage(errorType, message) {
            this.error = true;
            this.alertType = errorType;
            this.errorMessage = message;
        },
        hideErrorMessage() {
            this.error = false
            this.errorMessage = ""
            this.alertType = "alert-warning"
        },
        getWords() {
            var self = this;

            this.loading = true;

            var request = new XMLHttpRequest();
            request.onreadystatechange = function() {
                if (request.readyState == XMLHttpRequest.DONE) {
                    self.loading = false;

                    if (request.status == 200) {
                        self.words = JSON.parse(request.responseText).map((x) => x.toUpperCase());

                        if(self.words.length == 0)
                            self.showErrorMessage("alert-warning", "No results");
                        else
                            self.hideErrorMessage();
                    } else {
                        self.showErrorMessage("alert-danger", request.responseText);
                    }
                }
            };

            request.open("POST", "https://us-central1-lmontes.cloudfunctions.net/word-guesser");
            request.setRequestHeader("Content-Type", "application/json");

            var requestData = {
                "letters": this.letters.toUpperCase(),
                "language": this.language
            }

            request.send(JSON.stringify(requestData));
        }
    }
})
