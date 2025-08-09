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

    // Contact: detect location and map link
    const detectBtn = document.getElementById('detectLocationBtn');
    const locationInput = document.getElementById('contact-location') || document.getElementById('location');
    const openMapLink = document.getElementById('openMapLink');
    if (detectBtn && locationInput) {
        detectBtn.addEventListener('click', () => {
            if (!navigator.geolocation) {
                alert('আপনার ব্রাউজারে লোকেশন সাপোর্ট নেই');
                return;
            }
            detectBtn.disabled = true;
            detectBtn.innerText = 'লোকেশন নিচ্ছে...';
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const { latitude, longitude } = pos.coords;
                    const url = `https://maps.google.com/?q=${latitude},${longitude}`;
                    locationInput.value = `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
                    if (openMapLink) {
                        openMapLink.href = url;
                        openMapLink.style.display = 'inline-block';
                    }
                    detectBtn.disabled = false;
                    detectBtn.innerText = 'লোকেশন নিন';
                },
                (err) => {
                    alert('লোকেশন পাওয়া যায়নি: ' + err.message);
                    detectBtn.disabled = false;
                    detectBtn.innerText = 'লোকেশন নিন';
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        });
    }

    // Chat widget toggle
    const chatFab = document.getElementById('openChatFab');
    const chatWidget = document.getElementById('chatWidget');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const chatInput = document.getElementById('chatInput');

    function openChat() { if (chatWidget) chatWidget.classList.remove('hidden'); }
    function closeChat() { if (chatWidget) chatWidget.classList.add('hidden'); }

    if (chatFab) chatFab.addEventListener('click', openChat);
    if (closeChatBtn) closeChatBtn.addEventListener('click', closeChat);
    if (chatSendBtn && chatInput) {
        chatSendBtn.addEventListener('click', () => {
            if (!chatInput.value.trim()) return;
            alert('মেসেজ পাঠানো হয়েছে (ডেমো): ' + chatInput.value.trim());
            chatInput.value = '';
            chatInput.focus();
        });
    }

    // আরও ইন্টারেক্টিভ ফাংশন এখানে যোগ করা হবে (যেমন স্লাইডার, কার্ট ফাংশনালিটি)
});