document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chatBox');
    const form = document.getElementById('claimForm');
    const textarea = document.getElementById('id_claim');
    const quickButtons = document.querySelectorAll('.quick-btn');
    const clearButton = document.getElementById('clearChat');
    const currentLang = document.documentElement.lang || 'sw';

    const uiText = {
        sw: {
            selectedQuestion: 'Umechagua swali: “{question}”',
            welcome: 'Habari! Nimewekwa kukusadia kuchunguza dai la Kikiristo, maandiko, na teknolojia kwa usawaziko wa ushahidi.',
            prompt: 'Uliza swali kama: “666 ni chip ya ubongo?” au “AI ni mnyama wa Ufunuo?”',
            analyzing: 'Inachunguza ...'
        },
        en: {
            selectedQuestion: 'You selected: “{question}”',
            welcome: 'Hello! I am here to help investigate claims by separating scripture, history, and technology with evidence-driven analysis.',
            prompt: 'Ask a question like: “666 is a brain chip?” or “Is AI the beast of Revelation?”',
            analyzing: 'Analyzing ...'
        }
    };

    const text = uiText[currentLang] || uiText.sw;

    function addBotMessage(message) {
        if (!chatBox) return;
        const wrapper = document.createElement('div');
        wrapper.className = 'message bot';
        wrapper.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (quickButtons) {
        quickButtons.forEach((button) => {
            button.addEventListener('click', function () {
                const question = this.dataset.question;
                if (textarea) {
                    textarea.value = question;
                    textarea.focus();
                }
                addBotMessage(text.selectedQuestion.replace('{question}', question));
            });
        });
    }

    if (clearButton && chatBox) {
        clearButton.addEventListener('click', function () {
            chatBox.innerHTML = `
                <div class="message bot">
                    <p>${text.welcome}</p>
                </div>
                <div class="message bot">
                    <p>${text.prompt}</p>
                </div>
            `;
            if (textarea) textarea.value = '';
        });
    }

    if (form && textarea) {
        form.addEventListener('submit', function () {
            const value = textarea.value.trim();
            if (!value) {
                textarea.focus();
                return;
            }
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.innerHTML = `<p>${value}</p>`;
            chatBox.appendChild(userMessage);
            const statusMessage = document.createElement('div');
            statusMessage.className = 'message bot';
            statusMessage.innerHTML = `<p>${text.analyzing}</p>`;
            chatBox.appendChild(statusMessage);
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }
});
