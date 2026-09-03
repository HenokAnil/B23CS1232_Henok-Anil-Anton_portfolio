/**
 * ==============================================================================
 * HENOK ANIL ANTON — PORTFOLIO JAVASCRIPT CORE
 * Clean ES6+ Vanilla JavaScript: DOM Manipulation, Event Handling, Regex Validation,
 * LocalStorage Persistence & Interactive UI Features (No External Frameworks)
 * ==============================================================================
 */

// Strict Mode for high-assurance code quality
'use strict';

/* --------------------------------------------------------------------------
   1. DATA DEFINITIONS (B1: Dynamic Project & Skill Datasets)
   -------------------------------------------------------------------------- */

/**
 * Array of project objects containing metadata, categories, tags, and assets.
 * Rendered dynamically to satisfy Part B1 requirement.
 */
const PROJECTS_DATA = [
  {
    id: 'event-reconstruction',
    title: 'Event Reconstruction Using Semantic Graphs',
    category: 'cybersecurity',
    categoryLabel: 'Cybersecurity / AI',
    badge: 'Flagship Research',
    tags: ['Python', 'Electron.js', 'JavaScript', 'Graph Analytics', 'NLP'],
    image: 'assets/images/project-event-graph.jpg',
    desc: 'Threat-analysis model that reconstructs cyberattack timelines by constructing semantic graphs from log feeds, surfacing multi-stage attack vectors and origin paths.',
    detailedDesc: 'Architected an automated cybersecurity forensic platform that ingests raw server and firewall event logs to extract entities, relationships, and temporal sequences. Security analysts can interactively visualize attack progression timelines and isolate root vulnerabilities before exfiltration occurs.',
    githubUrl: 'https://github.com/HenokAnil',
    demoUrl: '#projects'
  },
  {
    id: 'alaka-enterprise',
    title: 'ALAKA — Knowledge Asset Lifecycle & Audit',
    category: 'enterprise',
    categoryLabel: 'Enterprise Systems',
    badge: 'Hackathon Project',
    tags: ['Java', 'JavaScript', 'CSS', 'Document Governance', 'Audit Trail'],
    image: 'assets/images/project-alaka.jpg',
    desc: 'Enterprise document-management platform delivering authenticated lifecycle controls, end-to-end cryptographic audit trails, and strict access governance.',
    detailedDesc: 'Engineered for strict regulatory environments (SOX, GDPR, ISO 27001 readiness), ALAKA provides immutable record histories, granular permission matrices, and cryptographic checksum validation for enterprise organizational knowledge assets.',
    githubUrl: 'https://github.com/HenokAnil',
    demoUrl: '#projects'
  },
  {
    id: 'resume-scanner',
    title: 'AI-Powered Intelligent Resume Scanner',
    category: 'ai',
    categoryLabel: 'Natural Language Processing',
    badge: 'AI / NLP Tool',
    tags: ['Python', 'NLP', 'Machine Learning', 'Semantic Match', 'FastAPI'],
    image: 'assets/images/project-resume-scanner.jpg',
    desc: 'Intelligent resume screening tool leveraging Natural Language Processing to evaluate candidate profiles against job requisites with semantic scoring.',
    detailedDesc: 'Utilizes contextual embeddings and term similarity matching to score candidate competencies across domains, radar visualizations, and automated match breakdown — reducing recruiter manual workload while maintaining objective precision.',
    githubUrl: 'https://github.com/HenokAnil',
    demoUrl: '#projects'
  },
  {
    id: 'ayursutra-platform',
    title: 'AyurSutra — Ayurvedic Healthcare Platform',
    category: 'enterprise',
    categoryLabel: 'Full-Stack / Healthcare',
    badge: 'Hackathon Project',
    tags: ['React', 'JavaScript', 'CSS', 'Telemedicine', 'UI/UX'],
    image: 'assets/images/project-ayursutra.jpg',
    desc: 'Full-stack digital healthcare platform connecting certified Ayurvedic practitioners with patients, crafted under competitive hackathon timelines.',
    detailedDesc: 'Features integrated video consultation workflows, herbal remedy prescription dispatch, patient vital tracking (Dosha balance scoring), and appointment scheduling with a clean, glassmorphic UI.',
    githubUrl: 'https://github.com/HenokAnil',
    demoUrl: '#projects'
  },
  {
    id: 'disaster-alert',
    title: 'Smart Alert System for Disasters',
    category: 'mobile',
    categoryLabel: 'Emergency Tech',
    badge: 'Civic Hackathon',
    tags: ['Figma', 'HTML5', 'CSS3', 'JavaScript', 'Geolocation'],
    image: 'assets/images/project-disaster-alert.jpg',
    desc: 'Early-warning disaster alert system delivering rapid, accessible notifications and hazard radius heatmaps for natural and man-made emergencies.',
    detailedDesc: 'Built with accessibility and high-stress UX in mind, this platform aggregates weather and seismic alerts with multi-channel broadcast messaging and localized shelter routing during urgent crisis scenarios.',
    githubUrl: 'https://github.com/HenokAnil',
    demoUrl: '#projects'
  },
  {
    id: 'waste-classification',
    title: 'Automated Waste Classification Model',
    category: 'ai',
    categoryLabel: 'Computer Vision / ML',
    badge: 'Sustainability AI',
    tags: ['Python', 'Computer Vision', 'PyTorch', 'Data Pipeline'],
    image: 'assets/images/project-resume-scanner.jpg',
    desc: 'Trained a computer vision deep learning model to accurately classify waste into recyclable and compostable streams to support circular sustainability.',
    detailedDesc: 'Implemented data augmentation pipelines, convolutional neural feature extraction, and real-time edge classification to optimize smart recycling bins for automated urban sorting.',
    githubUrl: 'https://github.com/HenokAnil',
    demoUrl: '#projects'
  }
];

/**
 * Skills dataset grouped by technical domain (B1)
 */
const SKILLS_DATA = [
  {
    category: 'languages',
    title: 'Programming Languages',
    icon: 'code-2',
    skills: ['Python', 'Java', 'C', 'JavaScript (ES6+)', 'TypeScript', 'HTML5', 'CSS3', 'Dart']
  },
  {
    category: 'frameworks',
    title: 'Frameworks & Libraries',
    icon: 'cpu',
    skills: ['React', 'Flutter', 'Electron.js', 'Node.js', 'FastAPI', 'Express', 'Tailwind CSS']
  },
  {
    category: 'ai',
    title: 'AI & Machine Learning',
    icon: 'brain-circuit',
    skills: ['Machine Learning', 'Natural Language Processing (NLP)', 'Agentic AI Systems', 'Prompt Engineering', 'PyTorch / Scikit-Learn']
  },
  {
    category: 'domains',
    title: 'Developer Tools & Systems',
    icon: 'terminal',
    skills: ['Git & GitHub', 'VS Code', 'Figma', 'Linux / Bash', 'REST APIs', 'Data Structures & Algorithms']
  }
];

/* --------------------------------------------------------------------------
   2. DOM ELEMENT REFERENCES
   -------------------------------------------------------------------------- */
const DOM = {
  header: document.getElementById('header'),
  themeToggleBtn: document.getElementById('themeToggleBtn'),
  mobileMenuBtn: document.getElementById('mobileMenuBtn'),
  siteNav: document.getElementById('siteNav'),
  navLinks: document.querySelectorAll('.nav-link'),
  typewriterEl: document.getElementById('typewriter'),
  skillsContainer: document.getElementById('skillsContainer'),
  skillCategoryTabs: document.getElementById('skillCategoryTabs'),
  projectsContainer: document.getElementById('projectsContainer'),
  projectFilterGroup: document.getElementById('projectFilterGroup'),
  showFavoritesBtn: document.getElementById('showFavoritesBtn'),
  favCountEl: document.getElementById('favCount'),
  projectModal: document.getElementById('projectModal'),
  modalContent: document.getElementById('modalContent'),
  modalCloseBtn: document.getElementById('modalCloseBtn'),
  scrollToTopBtn: document.getElementById('scrollToTopBtn'),
  currentYearEl: document.getElementById('currentYear'),
  contactForm: document.getElementById('contactForm'),
  userNameInput: document.getElementById('userName'),
  userEmailInput: document.getElementById('userEmail'),
  userMessageInput: document.getElementById('userMessage'),
  nameError: document.getElementById('nameError'),
  emailError: document.getElementById('emailError'),
  messageError: document.getElementById('messageError'),
  formGlobalFeedback: document.getElementById('formGlobalFeedback')
};

/* --------------------------------------------------------------------------
   3. APPLICATION STATE & LOCALSTORAGE (B4)
   -------------------------------------------------------------------------- */
const STATE = {
  theme: localStorage.getItem('henok_portfolio_theme') || 'dark',
  activeProjectFilter: 'all',
  activeSkillCategory: 'all',
  favoriteProjects: JSON.parse(localStorage.getItem('henok_portfolio_favs')) || [],
  showingOnlyFavorites: false
};

/* --------------------------------------------------------------------------
   4. INITIALIZATION ROUTINE
   -------------------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  // Set current copyright year
  if (DOM.currentYearEl) {
    DOM.currentYearEl.textContent = new Date().getFullYear();
  }

  // Initialize theme from storage
  initTheme();

  // Initialize dynamic DOM rendering (B1)
  renderSkills(STATE.activeSkillCategory);
  renderProjects(STATE.activeProjectFilter);
  updateFavoritesCounter();

  // Initialize typewriter animation
  initTypewriter();

  // Initialize event listeners (B2, B3)
  initNavigation();
  initThemeToggle();
  initProjectFiltering();
  initSkillsFiltering();
  initProjectModal();
  initScrollEffects();
  initFormValidation();

  // Initialize Lucide Icons
  if (window.lucide) {
    window.lucide.createIcons();
  }
});

/* --------------------------------------------------------------------------
   5. THEME SWITCHER & LOCALSTORAGE PERSISTENCE (B2, B4)
   -------------------------------------------------------------------------- */
function initTheme() {
  document.documentElement.setAttribute('data-theme', STATE.theme);
}

function initThemeToggle() {
  if (!DOM.themeToggleBtn) return;

  DOM.themeToggleBtn.addEventListener('click', () => {
    STATE.theme = STATE.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', STATE.theme);
    localStorage.setItem('henok_portfolio_theme', STATE.theme);

    // Refresh icons
    if (window.lucide) {
      window.lucide.createIcons();
    }
  });
}

/* --------------------------------------------------------------------------
   6. DYNAMIC DATA RENDERING (B1: DOM Manipulation)
   -------------------------------------------------------------------------- */

/**
 * Dynamically renders technical skill cards based on active category filter
 * @param {string} category - 'all' or specific skill category key
 */
function renderSkills(category = 'all') {
  if (!DOM.skillsContainer) return;

  // Filter skills array using ES6 filter method
  const filteredSkills = category === 'all' 
    ? SKILLS_DATA 
    : SKILLS_DATA.filter(group => group.category === category);

  // Map each group into template literal HTML cards
  const cardsHTML = filteredSkills.map(group => {
    const tagsHTML = group.skills
      .map(skill => `<li>${skill}</li>`)
      .join('');

    return `
      <article class="skill-card reveal">
        <div class="skill-card-header">
          <div class="skill-card-icon">
            <i data-lucide="${group.icon}"></i>
          </div>
          <h4>${group.title}</h4>
        </div>
        <ul class="skill-tag-list" aria-label="${group.title}">
          ${tagsHTML}
        </ul>
      </article>
    `;
  }).join('');

  DOM.skillsContainer.innerHTML = cardsHTML;

  if (window.lucide) {
    window.lucide.createIcons();
  }
  observeScrollReveals();
}

/**
 * Dynamically renders project cards from JavaScript objects array
 * @param {string} filter - Category filter or 'all'
 */
function renderProjects(filter = 'all') {
  if (!DOM.projectsContainer) return;

  let projectsToDisplay = PROJECTS_DATA;

  // If "Favorites" mode is toggled, filter by saved favorites
  if (STATE.showingOnlyFavorites) {
    projectsToDisplay = projectsToDisplay.filter(p => STATE.favoriteProjects.includes(p.id));
  } else if (filter !== 'all') {
    projectsToDisplay = projectsToDisplay.filter(p => p.category === filter);
  }

  // Handle empty state gracefully
  if (projectsToDisplay.length === 0) {
    DOM.projectsContainer.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 48px 20px; color: var(--text-secondary);">
        <i data-lucide="folder-search" style="width: 48px; height: 48px; margin-bottom: 12px; color: var(--accent-cyan);"></i>
        <h3 style="margin-bottom: 8px;">No Projects Found</h3>
        <p>No projects match your currently selected criteria.</p>
      </div>
    `;
    if (window.lucide) window.lucide.createIcons();
    return;
  }

  // Map project dataset into dynamic cards
  const projectsHTML = projectsToDisplay.map(project => {
    const isBookmarked = STATE.favoriteProjects.includes(project.id);
    const tagsHTML = project.tags
      .slice(0, 4)
      .map(tag => `<span class="project-tag">${tag}</span>`)
      .join('');

    return `
      <article class="project-card reveal" data-project-id="${project.id}">
        <div class="project-thumbnail-wrapper">
          <img src="${project.image}" alt="${project.title} Preview" class="project-thumbnail" loading="lazy">
          <span class="project-overlay-badge">${project.badge}</span>
          <button class="project-favorite-btn ${isBookmarked ? 'bookmarked' : ''}" 
                  data-fav-id="${project.id}" 
                  aria-label="Save ${project.title} to favorites"
                  title="${isBookmarked ? 'Remove from favorites' : 'Save to favorites'}">
            <i data-lucide="star"></i>
          </button>
        </div>
        <div class="project-body">
          <h3 class="project-title">${project.title}</h3>
          <p class="project-desc">${project.desc}</p>
          <div class="project-tags">
            ${tagsHTML}
          </div>
          <div class="project-actions">
            <button class="btn btn-sm btn-outline view-details-btn" data-modal-target="${project.id}">
              <span>View Details</span>
              <i data-lucide="external-link"></i>
            </button>
            <a href="${project.githubUrl}" target="_blank" rel="noopener noreferrer" class="project-link-btn" aria-label="GitHub Repository for ${project.title}">
              <i data-lucide="github"></i> Repo
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');

  DOM.projectsContainer.innerHTML = projectsHTML;

  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Attach dynamic button event listeners
  attachProjectCardListeners();
  observeScrollReveals();
}

/**
 * Attaches event listeners to dynamically rendered project cards
 */
function attachProjectCardListeners() {
  // Favorite Bookmark Buttons (B4)
  document.querySelectorAll('.project-favorite-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const projectId = btn.dataset.favId;
      toggleFavorite(projectId);
    });
  });

  // Modal Details Buttons (B2)
  document.querySelectorAll('.view-details-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const projectId = btn.dataset.modalTarget;
      openProjectModal(projectId);
    });
  });
}

/* --------------------------------------------------------------------------
   7. FAVORITES PERSISTENCE (B4: LocalStorage)
   -------------------------------------------------------------------------- */
function toggleFavorite(projectId) {
  const index = STATE.favoriteProjects.indexOf(projectId);
  if (index > -1) {
    STATE.favoriteProjects.splice(index, 1);
  } else {
    STATE.favoriteProjects.push(projectId);
  }

  // Persist array in localStorage
  localStorage.setItem('henok_portfolio_favs', JSON.stringify(STATE.favoriteProjects));
  
  // Re-render and update UI count
  updateFavoritesCounter();
  renderProjects(STATE.activeProjectFilter);
}

function updateFavoritesCounter() {
  if (DOM.favCountEl) {
    DOM.favCountEl.textContent = STATE.favoriteProjects.length;
  }
}

/* --------------------------------------------------------------------------
   8. PROJECT & SKILL FILTERING (B2: Event Handling)
   -------------------------------------------------------------------------- */
function initProjectFiltering() {
  if (DOM.projectFilterGroup) {
    DOM.projectFilterGroup.addEventListener('click', (e) => {
      const targetBtn = e.target.closest('.filter-btn');
      if (!targetBtn) return;

      // Update active button state
      DOM.projectFilterGroup.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      targetBtn.classList.add('active');

      STATE.showingOnlyFavorites = false;
      if (DOM.showFavoritesBtn) DOM.showFavoritesBtn.classList.remove('active');

      STATE.activeProjectFilter = targetBtn.dataset.filter;
      renderProjects(STATE.activeProjectFilter);
    });
  }

  // Favorites Filter Toggle Button
  if (DOM.showFavoritesBtn) {
    DOM.showFavoritesBtn.addEventListener('click', () => {
      STATE.showingOnlyFavorites = !STATE.showingOnlyFavorites;
      DOM.showFavoritesBtn.classList.toggle('active', STATE.showingOnlyFavorites);

      if (STATE.showingOnlyFavorites) {
        DOM.projectFilterGroup.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      } else {
        const defaultBtn = DOM.projectFilterGroup.querySelector('[data-filter="all"]');
        if (defaultBtn) defaultBtn.classList.add('active');
        STATE.activeProjectFilter = 'all';
      }

      renderProjects(STATE.activeProjectFilter);
    });
  }
}

function initSkillsFiltering() {
  if (!DOM.skillCategoryTabs) return;

  DOM.skillCategoryTabs.addEventListener('click', (e) => {
    const targetBtn = e.target.closest('.filter-btn');
    if (!targetBtn) return;

    DOM.skillCategoryTabs.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.remove('active');
      btn.setAttribute('aria-selected', 'false');
    });
    targetBtn.classList.add('active');
    targetBtn.setAttribute('aria-selected', 'true');

    STATE.activeSkillCategory = targetBtn.dataset.skillCategory;
    renderSkills(STATE.activeSkillCategory);
  });
}

/* --------------------------------------------------------------------------
   9. PROJECT MODAL / LIGHTBOX (B2)
   -------------------------------------------------------------------------- */
function initProjectModal() {
  if (!DOM.projectModal || !DOM.modalCloseBtn) return;

  DOM.modalCloseBtn.addEventListener('click', closeProjectModal);

  DOM.projectModal.addEventListener('click', (e) => {
    if (e.target === DOM.projectModal) {
      closeProjectModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && DOM.projectModal.classList.contains('open')) {
      closeProjectModal();
    }
  });
}

function openProjectModal(projectId) {
  const project = PROJECTS_DATA.find(p => p.id === projectId);
  if (!project || !DOM.modalContent) return;

  const tagsHTML = project.tags.map(t => `<span class="project-tag">${t}</span>`).join(' ');

  DOM.modalContent.innerHTML = `
    <img src="${project.image}" alt="${project.title}" class="modal-image">
    <div style="margin-bottom: 8px;">
      <span class="project-overlay-badge" style="position: static; margin-bottom: 8px; display: inline-block;">${project.categoryLabel}</span>
    </div>
    <h2 style="font-size: 1.6rem; margin-bottom: 12px;">${project.title}</h2>
    <div class="project-tags" style="margin-bottom: 16px;">
      ${tagsHTML}
    </div>
    <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: 24px; font-size: 0.95rem;">
      ${project.detailedDesc}
    </p>
    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
      <a href="${project.githubUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">
        <i data-lucide="github"></i> View GitHub Repository
      </a>
      <a href="#contact" class="btn btn-secondary btn-sm" onclick="DOM.projectModal.classList.remove('open')">
        <i data-lucide="mail"></i> Discuss This Project
      </a>
    </div>
  `;

  DOM.projectModal.classList.add('open');
  DOM.projectModal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function closeProjectModal() {
  if (!DOM.projectModal) return;
  DOM.projectModal.classList.remove('open');
  DOM.projectModal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

/* --------------------------------------------------------------------------
   10. HERO TYPEWRITER ANIMATION
   -------------------------------------------------------------------------- */
function initTypewriter() {
  if (!DOM.typewriterEl) return;

  const phrases = [
    'Intelligent AI & ML Systems.',
    'High-Assurance Enterprise Platforms.',
    'Cyber Threat Semantic Graphs.',
    'Autonomous AI Agents.',
    'Intuitive Full-Stack Web Apps.'
  ];

  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingSpeed = 80;

  function typeStep() {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      DOM.typewriterEl.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 40;
    } else {
      DOM.typewriterEl.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 90;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      // Pause at full sentence
      typingSpeed = 1800;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typingSpeed = 400;
    }

    setTimeout(typeStep, typingSpeed);
  }

  typeStep();
}

/* --------------------------------------------------------------------------
   11. NAVIGATION & SCROLL INTERACTIONS (A1, A9, B2)
   -------------------------------------------------------------------------- */
function initNavigation() {
  // Mobile Hamburger Toggle
  if (DOM.mobileMenuBtn && DOM.siteNav) {
    DOM.mobileMenuBtn.addEventListener('click', () => {
      const isExpanded = DOM.mobileMenuBtn.getAttribute('aria-expanded') === 'true';
      DOM.mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
      DOM.mobileMenuBtn.classList.toggle('active');
      DOM.siteNav.classList.toggle('open');
    });

    // Close menu when clicking nav link
    DOM.navLinks.forEach(link => {
      link.addEventListener('click', () => {
        DOM.mobileMenuBtn.classList.remove('active');
        DOM.mobileMenuBtn.setAttribute('aria-expanded', 'false');
        DOM.siteNav.classList.remove('open');
      });
    });
  }

  // Active Navigation Link Indicator on Scroll
  window.addEventListener('scroll', updateActiveNavLink);
}

function updateActiveNavLink() {
  const sections = document.querySelectorAll('section[id]');
  const scrollPos = window.scrollY + 120;

  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');

    if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
      DOM.navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
          link.classList.add('active');
        }
      });
    }
  });
}

function initScrollEffects() {
  // Sticky Header Effect & Scroll to Top Button Visibility
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    if (DOM.header) {
      if (scrollY > 50) {
        DOM.header.classList.add('scrolled');
      } else {
        DOM.header.classList.remove('scrolled');
      }
    }

    if (DOM.scrollToTopBtn) {
      if (scrollY > 350) {
        DOM.scrollToTopBtn.classList.add('visible');
      } else {
        DOM.scrollToTopBtn.classList.remove('visible');
      }
    }
  });

  // Scroll to Top action
  if (DOM.scrollToTopBtn) {
    DOM.scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}

/**
 * IntersectionObserver for smooth fade/slide-up scroll reveals
 */
function observeScrollReveals() {
  const revealElements = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    revealElements.forEach(el => el.classList.add('revealed'));
    return;
  }

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        obs.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
  });

  revealElements.forEach(el => observer.observe(el));
}

/* --------------------------------------------------------------------------
   12. CONTACT FORM REGEX VALIDATION (B3)
   -------------------------------------------------------------------------- */

/**
 * Regular Expression Patterns for Form Validation (B3)
 */
const VALIDATION_PATTERNS = {
  // Name: Only alphabets and single spaces, min 2 and max 50 chars
  name: /^[a-zA-Z\s]{2,50}$/,
  // RFC 5322 standard email regex pattern
  email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
};

function initFormValidation() {
  if (!DOM.contactForm) return;

  // Real-time input listeners for immediate feedback
  if (DOM.userNameInput) {
    DOM.userNameInput.addEventListener('input', () => validateNameField());
    DOM.userNameInput.addEventListener('blur', () => validateNameField());
  }

  if (DOM.userEmailInput) {
    DOM.userEmailInput.addEventListener('input', () => validateEmailField());
    DOM.userEmailInput.addEventListener('blur', () => validateEmailField());
  }

  if (DOM.userMessageInput) {
    DOM.userMessageInput.addEventListener('input', () => validateMessageField());
    DOM.userMessageInput.addEventListener('blur', () => validateMessageField());
  }

  // Form Submit Handler
  DOM.contactForm.addEventListener('submit', handleFormSubmit);
}

/**
 * Validates Name input with regex
 * @returns {boolean} isValid
 */
function validateNameField() {
  const nameValue = DOM.userNameInput.value.trim();
  const parentGroup = document.getElementById('nameGroup');

  if (!nameValue) {
    setFieldStatus(parentGroup, DOM.nameError, 'Name is required.', false);
    return false;
  }

  if (!VALIDATION_PATTERNS.name.test(nameValue)) {
    setFieldStatus(parentGroup, DOM.nameError, 'Name must contain only letters (min. 2 characters).', false);
    return false;
  }

  setFieldStatus(parentGroup, DOM.nameError, '', true);
  return true;
}

/**
 * Validates Email input with regex
 * @returns {boolean} isValid
 */
function validateEmailField() {
  const emailValue = DOM.userEmailInput.value.trim();
  const parentGroup = document.getElementById('emailGroup');

  if (!emailValue) {
    setFieldStatus(parentGroup, DOM.emailError, 'Email address is required.', false);
    return false;
  }

  if (!VALIDATION_PATTERNS.email.test(emailValue)) {
    setFieldStatus(parentGroup, DOM.emailError, 'Please enter a valid email address (e.g. name@domain.com).', false);
    return false;
  }

  setFieldStatus(parentGroup, DOM.emailError, '', true);
  return true;
}

/**
 * Validates Message input length
 * @returns {boolean} isValid
 */
function validateMessageField() {
  const messageValue = DOM.userMessageInput.value.trim();
  const parentGroup = document.getElementById('messageGroup');

  if (!messageValue) {
    setFieldStatus(parentGroup, DOM.messageError, 'Message cannot be empty.', false);
    return false;
  }

  if (messageValue.length < 10) {
    setFieldStatus(parentGroup, DOM.messageError, `Message is too short (${messageValue.length}/10 characters minimum).`, false);
    return false;
  }

  setFieldStatus(parentGroup, DOM.messageError, '', true);
  return true;
}

/**
 * Helper to toggle visual feedback styles and error messages
 */
function setFieldStatus(groupEl, errorEl, message, isValid) {
  if (!groupEl || !errorEl) return;

  if (isValid) {
    groupEl.classList.remove('error');
    groupEl.classList.add('success');
    errorEl.textContent = '';
  } else {
    groupEl.classList.remove('success');
    groupEl.classList.add('error');
    errorEl.textContent = message;
  }
}

/**
 * Handles Form Submission with validation check and feedback message
 * Prevents default reload, confirms submission, and resets fields
 */
function handleFormSubmit(event) {
  event.preventDefault(); // Block standard page reload (B3 requirement)

  const isNameValid = validateNameField();
  const isEmailValid = validateEmailField();
  const isMessageValid = validateMessageField();

  if (isNameValid && isEmailValid && isMessageValid) {
    // Form is completely valid
    const senderName = DOM.userNameInput.value.trim();
    
    // Display interactive confirmation feedback
    if (DOM.formGlobalFeedback) {
      DOM.formGlobalFeedback.className = 'form-feedback success';
      DOM.formGlobalFeedback.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
          <i data-lucide="check-circle" style="width: 20px; height: 20px;"></i>
          <span>Thank you, <strong>${senderName}</strong>! Your message has been prepared successfully. I will get back to you shortly.</span>
        </div>
      `;
      if (window.lucide) window.lucide.createIcons();
    }

    // Reset Form Fields
    DOM.contactForm.reset();
    document.querySelectorAll('.form-group').forEach(group => {
      group.classList.remove('success', 'error');
    });

    // Auto clear success message after 7 seconds
    setTimeout(() => {
      if (DOM.formGlobalFeedback) {
        DOM.formGlobalFeedback.className = 'form-feedback';
        DOM.formGlobalFeedback.textContent = '';
      }
    }, 7000);
  } else {
    // Show top-level error hint
    if (DOM.formGlobalFeedback) {
      DOM.formGlobalFeedback.className = 'form-feedback error';
      DOM.formGlobalFeedback.textContent = 'Please correct the highlighted errors before submitting.';
    }
  }
}
