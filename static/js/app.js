// State
let currentTab = 'linkedin';

function switchTab(tab) {
    currentTab = tab;
    // Update Stepper
    document.querySelectorAll('.step-item').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    if (tab === 'linkedin') document.getElementById('step-1').classList.add('active');
    if (tab === 'process') document.getElementById('step-2').classList.add('active');
    if (tab === 'download') document.getElementById('step-3').classList.add('active');

    document.getElementById('content-' + tab).classList.add('active');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toast-icon');
    const msg = document.getElementById('toast-message');

    toast.className = 'toast ' + type;
    icon.textContent = type === 'success' ? '✅' : '❌';
    msg.textContent = message;

    toast.classList.add('visible');
    setTimeout(() => { toast.classList.remove('visible'); }, 5000);
}

// Feature: Import from Paste
function importFromPaste() {
    const content = document.getElementById('linkedin-paste-area').value.trim();
    if (!content) {
        showToast('Please paste content first', 'error');
        return;
    }

    const btn = document.getElementById('import-btn');
    btn.disabled = true;
    btn.textContent = 'Analyzing Profile...';

    fetch('/api/linkedin/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile_text: content })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showToast('Profile imported and synchronized!', 'success');
                btn.disabled = false;
                btn.textContent = 'Import Profile ✨';
                // Auto switch to next step
                setTimeout(() => {
                    switchTab('process');
                }, 1500);
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(err => {
            showToast(err.message || 'Error importing profile', 'error');
            btn.disabled = false;
            btn.textContent = 'Import Profile ✨';
        });
}

// Feature: Process Job
function processJob() {
    const jobDesc = document.getElementById('job-desc-area').value.trim();
    if (jobDesc.length < 50) {
        showToast('Job description is too short!', 'error');
        return;
    }

    // UI Transitions
    document.getElementById('job-input-view').style.display = 'none';
    document.getElementById('loading-box').style.display = 'flex';
    document.getElementById('results-box').style.display = 'none';

    let progress = 0;
    const progBar = document.getElementById('progress-fill');
    const statusText = document.getElementById('loading-status-text');

    const timer = setInterval(() => {
        progress += Math.random() * 5;
        if (progress > 95) progress = 95;
        progBar.style.width = progress + '%';

        if (progress > 20) statusText.innerText = 'Extracting ATS Keywords...';
        if (progress > 50) statusText.innerText = 'Matching with your Experience...';
        if (progress > 80) statusText.innerText = 'Building Professional DOCX...';
    }, 800);

    fetch('/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jobDesc })
    })
        .then(res => res.json())
        .then(data => {
            clearInterval(timer);
            progBar.style.width = '100%';

            if (data.success) {
                setTimeout(() => {
                    document.getElementById('loading-box').style.display = 'none';
                    document.getElementById('results-box').style.display = 'block';

                    document.getElementById('result-score').innerText = Math.round(data.match_score.overall_score);

                    // Metrics
                    const grid = document.getElementById('metrics-grid');
                    grid.innerHTML = `
                    <div class="metric-item">
                        <div class="metric-label">Skills Matched</div>
                        <div class="metric-value">${data.match_score.required_skills_matched}/${data.match_score.required_skills_total}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Keywords Found</div>
                        <div class="metric-value">${data.match_score.keywords_matched}</div>
                    </div>
                `;

                    document.getElementById('dl-cv').href = '/api/download/' + data.cv_file;
                    document.getElementById('dl-cl').href = '/api/download/' + data.cover_letter_file;
                    document.getElementById('dl-btn-cv').href = '/api/download/' + data.cv_file;
                    document.getElementById('dl-btn-cl').href = '/api/download/' + data.cover_letter_file;


                    showToast('Application generated successfully!', 'success');

                    // Activate Step 3
                    setTimeout(() => {
                        switchTab('download');
                        document.getElementById('step-3').classList.add('completed');
                    }, 500);
                    // Block removed to fix duplication
                }, 500);
            } else {
                showToast(data.error, 'error');
                document.getElementById('job-input-view').style.display = 'grid';
                document.getElementById('loading-box').style.display = 'none';
            }
        })
        .catch(err => {
            clearInterval(timer);
            showToast('Network error during generation', 'error');
            document.getElementById('job-input-view').style.display = 'grid';
            document.getElementById('loading-box').style.display = 'none';
        });
}

// Import Mode Toggle
function setImportMode(mode) {
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('btn-mode-' + mode).classList.add('active');

    ['paste', 'url', 'pdf'].forEach(m => {
        document.getElementById('view-' + m).style.display = (m === mode) ? (m === 'url' ? 'flex' : (m === 'pdf' ? 'flex' : 'block')) : 'none';
    });
}

function importFromUrl() {
    const url = document.getElementById('linkedin-url-input').value.trim();
    if (!url) return showToast('Please enter a valid URL', 'error');

    const btn = document.getElementById('import-url-btn');
    const originalText = btn.innerHTML;
    btn.textContent = 'Scraping... ⏳';
    btn.disabled = true;

    fetch('/api/linkedin/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ linkedin_url: url })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showToast('Profile scraped successfully!', 'success');
                setTimeout(() => location.reload(), 1500); // Reload to show profile state
            } else {
                throw new Error(data.error || 'Scraping failed');
            }
        })
        .catch(err => {
            showToast(err.message, 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
}

// PDF Import Logic
function handlePdfSelect() {
    const file = document.getElementById('pdf-upload-input').files[0];
    const nameDiv = document.getElementById('pdf-file-name');
    const btn = document.getElementById('import-pdf-btn');

    if (file) {
        nameDiv.textContent = file.name;
        nameDiv.style.display = 'block';
        btn.style.display = 'inline-block';
    } else {
        nameDiv.style.display = 'none';
        btn.style.display = 'none';
    }
}

function importFromPdf() {
    const file = document.getElementById('pdf-upload-input').files[0];
    if (!file) return showToast('No file selected', 'error');

    const btn = document.getElementById('import-pdf-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Analyzing... ⏳';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/import/pdf', {
        method: 'POST',
        body: formData // No headers for FormData, browser sets multipart
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showToast('PDF Profile imported!', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                throw new Error(data.error || 'Import failed');
            }
        })
        .catch(err => {
            showToast(err.message, 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
}

// Profile Management
function clearProfile() {
    if (confirm('Are you sure you want to disconnect this profile?')) {
        fetch('/api/profile/clear', { method: 'POST' })
            .then(() => location.reload())
            .catch(() => location.reload()); // Fallback
    }
}

// Profile Modal Logic
function openProfileEditor() {
    document.getElementById('profile-modal').style.display = 'flex';
    // Pre-fill
    fetch('/api/profile')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('p-name').value = data.profile.personal_info.name;
                document.getElementById('p-email').value = data.profile.personal_info.email;
                document.getElementById('p-summary').value = data.profile.summary;
            }
        });
}

function closeProfileEditor() {
    document.getElementById('profile-modal').style.display = 'none';
}

function saveProfile() {
    const profile = {
        personal_info: {
            name: document.getElementById('p-name').value,
            email: document.getElementById('p-email').value,
        },
        summary: document.getElementById('p-summary').value
    };

    fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile: profile })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showToast('Profile updated!', 'success');
                closeProfileEditor();
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast(data.error || 'Failed to update profile', 'error');
            }
        })
        .catch(err => {
            showToast('Network error saving profile', 'error');
        });
}

// Scroll Animation Observer
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll, .timeline-item').forEach(el => {
        observer.observe(el);
    });

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            document.querySelector('nav').classList.add('scrolled');
        } else {
            document.querySelector('nav').classList.remove('scrolled');
        }
    });
});
// Auth Logic
function openLoginModal() {
    document.getElementById('login-modal').style.display = 'flex';
}

function loginUser() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                showToast(data.error || 'Login failed', 'error');
            }
        })
        .catch(() => showToast('Network Error', 'error'));
}

function logoutUser() {
    fetch('/auth/logout', { method: 'POST' })
        .then(() => location.reload());
}
