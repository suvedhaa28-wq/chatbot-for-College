/* College Examination FAQ Assistant - Frontend Application Logic */

// Global State
let allAdminFAQs = [];

document.addEventListener('DOMContentLoaded', () => {
    // Render Welcome Message on Initialization
    renderWelcomeMessage();
    
    // Attach Enter Key Listener on Chat Input
    const userInput = document.getElementById('user-input');
    if (userInput) {
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Load initial admin stats
    fetchStats();
});

/**
 * Switch View Tabs (Student Chatbot vs Admin Manager)
 */
function switchTab(tabName) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.view-panel').forEach(panel => panel.classList.remove('active'));

    if (tabName === 'student') {
        document.getElementById('tab-student-btn').classList.add('active');
        document.getElementById('student-view').classList.add('active');
    } else {
        document.getElementById('tab-admin-btn').classList.add('active');
        document.getElementById('admin-view').classList.add('active');
        fetchStats();
        fetchAdminFAQs();
    }
}

/**
 * Renders initial welcome message required by prompt requirements
 */
function renderWelcomeMessage() {
    const chatContainer = document.getElementById('chat-messages');
    chatContainer.innerHTML = '';

    const welcomeText = "Hello! I'm your College Examination FAQ Assistant. Ask me anything about examinations, schedules, hall tickets, results, attendance requirements, or examination procedures.";
    
    appendBotMessage(welcomeText, 'welcome', 1.0, [
        "When are the semester exams?",
        "How can I download my hall ticket?",
        "What is the examination fee?",
        "What is the attendance requirement?",
        "When will results be published?",
        "How can I apply for revaluation?"
    ]);
}

/**
 * Sends student message to backend NLP API
 */
async function sendMessage(textOverride = null) {
    const inputElement = document.getElementById('user-input');
    const query = textOverride ? textOverride : inputElement.value.trim();

    if (!query) return;

    // Clear input field if from text box
    if (!textOverride) inputElement.value = '';

    // Append User Message Bubble
    appendUserMessage(query);

    // Show Typing Indicator
    showTypingIndicator(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: query })
        });

        const data = await response.json();

        // Simulate realistic typing delay (400ms)
        setTimeout(() => {
            showTypingIndicator(false);
            appendBotMessage(
                data.response,
                data.intent,
                data.confidence,
                data.suggestions
            );
        }, 400);

    } catch (error) {
        showTypingIndicator(false);
        appendBotMessage("Error connecting to server. Please check your network connection.", "error", 0, []);
    }
}

/**
 * Appends User message bubble to chat window
 */
function appendUserMessage(text) {
    const chatContainer = document.getElementById('chat-messages');
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const msgHtml = `
        <div class="message-row user">
            <div class="msg-avatar"><i class="fa-solid fa-user"></i></div>
            <div class="bubble-wrapper">
                <div class="bubble">${escapeHtml(text)}</div>
                <div class="msg-footer">
                    <span>${timeStr}</span>
                </div>
            </div>
        </div>
    `;

    chatContainer.insertAdjacentHTML('beforeend', msgHtml);
    scrollToBottom();
}

/**
 * Appends Chatbot message bubble with intent tag & suggested questions
 */
function appendBotMessage(text, intent, confidence, suggestions = []) {
    const chatContainer = document.getElementById('chat-messages');
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    let tagHtml = intent && intent !== 'welcome' && intent !== 'fallback' 
        ? `<span class="intent-tag"><i class="fa-solid fa-tag"></i> ${intent}</span>` 
        : '';

    let confidenceHtml = confidence > 0 
        ? `<span title="NLP Matching Confidence Score">Score: ${Math.round(confidence * 100)}%</span>` 
        : '';

    const msgHtml = `
        <div class="message-row bot">
            <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="bubble-wrapper">
                <div class="bubble">${formatLineBreaks(escapeHtml(text))}</div>
                <div class="msg-footer">
                    <span>${timeStr}</span>
                    ${tagHtml}
                    ${confidenceHtml}
                </div>
            </div>
        </div>
    `;

    chatContainer.insertAdjacentHTML('beforeend', msgHtml);

    // Update Suggested Questions Bar
    renderSuggestedChips(suggestions);
    scrollToBottom();
}

/**
 * Renders quick suggested questions chips below chat input
 */
function renderSuggestedChips(suggestions) {
    const container = document.getElementById('chips-wrapper');
    container.innerHTML = '';

    if (!suggestions || suggestions.length === 0) return;

    suggestions.forEach(questionText => {
        const btn = document.createElement('button');
        btn.className = 'chip-btn';
        btn.innerHTML = `<i class="fa-solid fa-arrow-right-long"></i> ${escapeHtml(questionText)}`;
        btn.onclick = () => sendMessage(questionText);
        container.appendChild(btn);
    });
}

/**
 * Toggle Typing Indicator Visibility
 */
function showTypingIndicator(show) {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.style.display = show ? 'flex' : 'none';
        if (show) scrollToBottom();
    }
}

/**
 * Clear Chat History
 */
function clearChat() {
    renderWelcomeMessage();
}

/**
 * Auto-scroll chat container to bottom
 */
function scrollToBottom() {
    const container = document.getElementById('chat-messages');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

/* ==========================================================================
   ADMIN FAQ MANAGEMENT JAVASCRIPT FUNCTIONS
   ========================================================================== */

async function fetchStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        if (data.success) {
            document.getElementById('stat-total-faqs').innerText = data.total_faqs;
            document.getElementById('stat-total-categories').innerText = data.total_categories;
            document.getElementById('stat-total-intents').innerText = data.total_intents;
            document.getElementById('stat-total-patterns').innerText = data.total_patterns;
        }
    } catch (e) { console.error("Error fetching stats:", e); }
}

async function fetchAdminFAQs() {
    try {
        const res = await fetch('/api/faqs');
        const data = await res.json();

        if (data.success) {
            allAdminFAQs = data.faqs;
            
            // Populate category select dropdown
            const catSelect = document.getElementById('admin-category-filter');
            catSelect.innerHTML = '<option value="">All Categories</option>';
            data.categories.forEach(cat => {
                catSelect.innerHTML += `<option value="${escapeHtml(cat)}">${escapeHtml(cat)}</option>`;
            });

            renderAdminTable(allAdminFAQs);
        }
    } catch (e) { console.error("Error fetching FAQs:", e); }
}

function renderAdminTable(faqsList) {
    const tbody = document.getElementById('faq-table-body');
    tbody.innerHTML = '';

    if (faqsList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 20px; color: #64748b;">No FAQs found.</td></tr>';
        return;
    }

    faqsList.forEach(faq => {
        const patternsStr = faq.patterns ? faq.patterns.slice(0, 3).join(', ') : '';

        const row = `
            <tr>
                <td><strong>#${faq.id}</strong></td>
                <td><span class="badge" style="background:#e0f2fe; color:#0369a1;">${escapeHtml(faq.category || 'General')}</span></td>
                <td><code>${escapeHtml(faq.intent)}</code></td>
                <td>
                    <strong>${escapeHtml(faq.question)}</strong><br>
                    <small style="color: #64748b;">${escapeHtml(faq.response.substring(0, 110))}...</small>
                </td>
                <td style="text-align: center;">
                    <button class="action-icon-btn edit" onclick="openEditFAQModal(${faq.id})" title="Edit FAQ"><i class="fa-solid fa-pen-to-square"></i></button>
                    <button class="action-icon-btn delete" onclick="deleteFAQ(${faq.id})" title="Delete FAQ"><i class="fa-solid fa-trash-can"></i></button>
                </td>
            </tr>
        `;
        tbody.insertAdjacentHTML('beforeend', row);
    });
}

function filterFAQs() {
    const searchVal = document.getElementById('admin-search').value.toLowerCase().strip();
    const catVal = document.getElementById('admin-category-filter').value;

    let filtered = allAdminFAQs.filter(f => {
        const matchesSearch = !searchVal || 
            f.question.toLowerCase().includes(searchVal) ||
            f.intent.toLowerCase().includes(searchVal) ||
            f.response.toLowerCase().includes(searchVal);

        const matchesCat = !catVal || f.category === catVal;

        return matchesSearch && matchesCat;
    });

    renderAdminTable(filtered);
}

function openAddFAQModal() {
    document.getElementById('modal-title').innerText = "Add New Examination FAQ";
    document.getElementById('faq-id').value = "";
    document.getElementById('faq-intent').value = "";
    document.getElementById('faq-category').value = "";
    document.getElementById('faq-question').value = "";
    document.getElementById('faq-patterns').value = "";
    document.getElementById('faq-response').value = "";

    document.getElementById('faq-modal').style.display = 'flex';
}

function openEditFAQModal(faqId) {
    const faq = allAdminFAQs.find(f => f.id === faqId);
    if (!faq) return;

    document.getElementById('modal-title').innerText = `Edit Examination FAQ #${faq.id}`;
    document.getElementById('faq-id').value = faq.id;
    document.getElementById('faq-intent').value = faq.intent;
    document.getElementById('faq-category').value = faq.category || "General";
    document.getElementById('faq-question').value = faq.question;
    document.getElementById('faq-patterns').value = faq.patterns ? faq.patterns.join(', ') : "";
    document.getElementById('faq-response').value = faq.response;

    document.getElementById('faq-modal').style.display = 'flex';
}

function closeFAQModal() {
    document.getElementById('faq-modal').style.display = 'none';
}

async function handleFAQFormSubmit(event) {
    event.preventDefault();

    const faqId = document.getElementById('faq-id').value;
    const payload = {
        intent: document.getElementById('faq-intent').value.trim(),
        category: document.getElementById('faq-category').value.trim(),
        question: document.getElementById('faq-question').value.trim(),
        patterns: document.getElementById('faq-patterns').value.split(',').map(s => s.trim()).filter(Boolean),
        response: document.getElementById('faq-response').value.trim()
    };

    try {
        let url = '/api/faqs';
        let method = 'POST';

        if (faqId) {
            url = `/api/faqs/${faqId}`;
            method = 'PUT';
        }

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
            closeFAQModal();
            fetchStats();
            fetchAdminFAQs();
        } else {
            alert("Error: " + data.message);
        }
    } catch (e) {
        alert("Server error submitting form.");
    }
}

async function deleteFAQ(faqId) {
    if (!confirm("Are you sure you want to delete this FAQ entry?")) return;

    try {
        const res = await fetch(`/api/faqs/${faqId}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            fetchStats();
            fetchAdminFAQs();
        } else {
            alert("Error deleting FAQ: " + data.message);
        }
    } catch (e) { alert("Error connecting to server."); }
}

// Utility Helper Functions
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;")
              .replace(/</g, "&lt;")
              .replace(/>/g, "&gt;")
              .replace(/"/g, "&quot;")
              .replace(/'/g, "&#039;");
}

function formatLineBreaks(str) {
    return str.replace(/\n/g, '<br>');
}
