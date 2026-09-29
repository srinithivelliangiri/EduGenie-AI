const taskSelect = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitButton = document.getElementById("submitButton");
const loading = document.getElementById("loading");
const resultContent = document.getElementById("resultContent");


function showResult(text) {
    resultContent.textContent = text;
}


function showError(message) {
    resultContent.textContent = "Error: " + message;
}


function setLoading(isLoading) {
    if (isLoading) {
        loading.classList.remove("hidden");
        submitButton.disabled = true;
        submitButton.textContent = "Generating...";
    } else {
        loading.classList.add("hidden");
        submitButton.disabled = false;
        submitButton.textContent = "Generate";
    }
}


function formatQuiz(quiz) {
    if (!quiz.questions) {
        return JSON.stringify(quiz, null, 2);
    }

    let output = "";

    quiz.questions.forEach(function(question, index) {

        output += "Question " + (index + 1) + "\n";
        output += question.question + "\n\n";

        question.options.forEach(function(option, optionIndex) {
            output +=
                String.fromCharCode(65 + optionIndex) +
                ". " +
                option +
                "\n";
        });

        output += "\n";
        output += "Correct answer: " +
            question.correct_answer +
            "\n";

        output += "Explanation: " +
            question.explanation +
            "\n\n";

        output += "-------------------------\n\n";
    });

    return output;
}


function formatLearningPath(data) {

    let output = "";

    output += data.title + "\n\n";

    output += data.overview + "\n\n";

    output += "Estimated duration: " +
        data.estimated_duration +
        "\n\n";

    if (data.stages) {

        data.stages.forEach(function(stage) {

            output += "===== " +
                stage.level +
                " =====\n\n";

            output += "Topics:\n";

            stage.topics.forEach(function(topic) {
                output += "- " + topic + "\n";
            });

            output += "\nGoals:\n";

            stage.goals.forEach(function(goal) {
                output += "- " + goal + "\n";
            });

            output += "\nResources:\n";

            stage.resources.forEach(function(resource) {
                output += "- " + resource + "\n";
            });

            output += "\nPractice:\n";

            stage.practice.forEach(function(practice) {
                output += "- " + practice + "\n";
            });

            output += "\n";
        });
    }

    return output;
}


async function callAPI(endpoint, data) {

    const response = await fetch(endpoint, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const responseText = await response.text();

    let result;

    try {
        result = JSON.parse(responseText);
    } catch (error) {

        throw new Error(
            "Server returned an invalid response."
        );
    }


    if (!response.ok) {

        throw new Error(
            result.detail ||
            "The server returned an error."
        );
    }


    return result;
}


async function handleSubmit() {

    const task = taskSelect.value;
    const text = inputText.value.trim();


    if (!text) {

        showError(
            "Please enter a question, topic, or text."
        );

        return;
    }


    setLoading(true);

    showResult("");


    try {

        let result;


        if (task === "qa") {

            result = await callAPI(
                "/qa",
                {
                    question: text
                }
            );

            showResult(result.answer);
        }


        else if (task === "explain") {

            result = await callAPI(
                "/explain",
                {
                    topic: text
                }
            );

            showResult(result.explanation);
        }


        else if (task === "quiz") {

            result = await callAPI(
                "/quiz",
                {
                    text: text
                }
            );

            showResult(
                formatQuiz(result)
            );
        }


        else if (task === "summarize") {

            result = await callAPI(
                "/summarize",
                {
                    text: text
                }
            );

            showResult(result.summary);
        }


        else if (task === "learning") {

            result = await callAPI(
                "/learn/recommendations",
                {
                    topic: text
                }
            );

            showResult(
                formatLearningPath(result)
            );
        }


    } catch (error) {

        showError(
            error.message
        );

    } finally {

        setLoading(false);

    }
}


submitButton.addEventListener(
    "click",
    handleSubmit
);