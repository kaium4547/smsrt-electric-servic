// এই ফাইলটি আপনার ওয়েবসাইটের ইন্টারেক্টিভ ফাংশনালিটি নিয়ন্ত্রণ করবে।

document.addEventListener('DOMContentLoaded', function() {
    // উদাহরণস্বরূপ: লগইন ফর্ম সাবমিট হ্যান্ডলার (প্রাথমিক, কোন ব্যাকএন্ড ইন্টিগ্রেশন ছাড়া)
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault(); // ফর্ম সাবমিট বন্ধ করা
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            console.log('Login Attempt:');
            console.log('Email:', email);
            console.log('Password:', password);

            alert('লগইন করার চেষ্টা চলছে... (এই মুহূর্তে ব্যাকএন্ড সংযুক্ত নয়)');
            // এখানে ব্যাকএন্ডে ডেটা পাঠানোর কোড যুক্ত হবে
        });
    }

    // উদাহরণস্বরূপ: সাইনআপ ফর্ম সাবমিট হ্যান্ডলার
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault(); // ফর্ম সাবমিট বন্ধ করা
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const userType = document.querySelector('input[name="userType"]:checked').value;

            if (password !== confirmPassword) {
                alert('পাসওয়ার্ড দুটি মিলছে না!');
                return;
            }

            console.log('Signup Attempt:');
            console.log('Name:', name);
            console.log('Email:', email);
            console.log('Phone:', phone);
            console.log('Password:', password);
            console.log('User Type:', userType);

            alert('সাইনআপ করার চেষ্টা চলছে... (এই মুহূর্তে ব্যাকএন্ড সংযুক্ত নয়)');
            // এখানে ব্যাকএন্ডে ডেটা পাঠানোর কোড যুক্ত হবে
        });
    }

    // ড্যাশবোর্ড সাইডবার ন্যাভিগেশন
    const dashboardSidebar = document.querySelector('.dashboard-sidebar ul');
    const dashboardPanels = document.querySelectorAll('.dashboard-panel');

    if (dashboardSidebar) {
        dashboardSidebar.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                e.preventDefault();
                const targetId = e.target.getAttribute('href').substring(1);

                // Remove active class from all links and panels
                dashboardSidebar.querySelectorAll('a').forEach(link => link.classList.remove('active'));
                dashboardPanels.forEach(panel => panel.classList.remove('active'));

                // Add active class to clicked link and corresponding panel
                e.target.classList.add('active');
                document.getElementById(targetId).classList.add('active');
            }
        });
    }

    // লাইভ চ্যাট খোলার ফাংশন (Tawk.to বা অন্য চ্যাটবক্সের জন্য)
    window.openLiveChat = function() {
        alert('লাইভ চ্যাট ফাংশন এখনো সংযুক্ত করা হয়নি। ভবিষ্যতে এখানে চ্যাটবক্স আসবে।');
        // এখানে Tawk.to বা অন্যান্য লাইভ চ্যাট সার্ভিস এর JavaScript কোড যুক্ত হবে।
        // উদাহরণস্বরূপ: Tawk_API.toggle();
    };

    // আরও ইন্টারেক্টিভ ফাংশন এখানে যোগ করা হবে (যেমন স্লাইডার, কার্ট ফাংশনালিটি)
});

// Hero Slider Logic
(function() {
  function initHeroSlider() {
    const slider = document.querySelector('.hero-slider');
    if (!slider) return;

    const slides = slider.querySelectorAll('.slide');
    const prevBtn = slider.querySelector('.slider-control.prev');
    const nextBtn = slider.querySelector('.slider-control.next');
    const dotsContainer = slider.querySelector('.slider-dots');

    if (slides.length === 0) return;

    let current = 0;
    let timer = null;
    const AUTOPLAY_MS = 5000;

    // Build dots
    dotsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('button');
      dot.className = 'slider-dot' + (idx === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `Go to slide ${idx + 1}`);
      dot.addEventListener('click', () => goTo(idx));
      dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll('.slider-dot');

    function setActive(index) {
      slides.forEach((s, i) => s.classList.toggle('active', i === index));
      dots.forEach((d, i) => d.classList.toggle('active', i === index));
    }

    function goTo(index) {
      current = (index + slides.length) % slides.length;
      setActive(current);
      restartAutoplay();
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    function startAutoplay() {
      if (timer) clearInterval(timer);
      if (slides.length > 1) {
        timer = setInterval(next, AUTOPLAY_MS);
      }
    }
    function restartAutoplay() {
      if (!timer) return startAutoplay();
      clearInterval(timer);
      startAutoplay();
    }

    prevBtn?.addEventListener('click', prev);
    nextBtn?.addEventListener('click', next);

    // Pause on hover for desktop
    slider.addEventListener('mouseenter', () => { if (timer) clearInterval(timer); });
    slider.addEventListener('mouseleave', startAutoplay);

    // Initialize
    setActive(current);
    startAutoplay();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeroSlider);
  } else {
    initHeroSlider();
  }
})();

// Service Request Modal + Submit
(function(){
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  function initServiceRequestModal(){
    const modal = document.getElementById('serviceRequestModal');
    if (!modal) return;
    const form = document.getElementById('serviceRequestForm');
    const successBox = document.getElementById('requestSuccess');
    const serviceIdInput = document.getElementById('requestServiceId');
    const titleEl = document.getElementById('requestModalTitle');

    function openModal(serviceId, serviceName){
      serviceIdInput.value = serviceId;
      titleEl.textContent = `সার্ভিস রিকোয়েস্ট - ${serviceName}`;
      modal.classList.add('show');
      modal.style.display = 'block';
    }
    function closeModal(){
      modal.classList.remove('show');
      modal.style.display = 'none';
      successBox.style.display = 'none';
      form.reset();
    }

    document.querySelectorAll('[data-open-request-modal]').forEach(btn => {
      btn.addEventListener('click', () => {
        const sid = btn.getAttribute('data-service-id');
        const sname = btn.getAttribute('data-service-name') || 'Service';
        openModal(sid, sname);
      });
    });
    modal.querySelectorAll('[data-close-request-modal]').forEach(el => el.addEventListener('click', closeModal));

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      try {
        const resp = await fetch(form.action, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') || '' },
          body: formData,
        });
        if (!resp.ok) throw new Error('Network error');
        const data = await resp.json();
        if (data.success) {
          successBox.style.display = 'block';
          setTimeout(() => { closeModal(); }, 1500);
        } else {
          alert('দুঃখিত, রিকোয়েস্ট নেয়া যায়নি। পরে চেষ্টা করুন');
        }
      } catch(err) {
        alert('সমস্যা হয়েছে। পরে চেষ্টা করুন');
        console.error(err);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initServiceRequestModal);
  } else {
    initServiceRequestModal();
  }
})();