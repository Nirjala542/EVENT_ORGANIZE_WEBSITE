// Image carousel for hero section
const carouselImages = [
  'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
  'https://images.unsplash.com/photo-1540575467063-178f50902556?w=600&h=400&fit=crop',
  'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600&h=400&fit=crop'
];

let currentImageIndex = 0;

function initCarousel() {
  const carousel = document.getElementById('hero-carousel');
  if (!carousel) return;

  // Create image elements
  carouselImages.forEach((imgUrl, idx) => {
    const img = document.createElement('img');
    img.src = imgUrl;
    img.className = 'carousel-img' + (idx === 0 ? ' active' : '');
    img.alt = 'event ' + idx;
    carousel.appendChild(img);
  });

  // Rotate every 5 seconds
  setInterval(() => {
    const imgs = carousel.querySelectorAll('.carousel-img');
    imgs[currentImageIndex].classList.remove('active');
    currentImageIndex = (currentImageIndex + 1) % carouselImages.length;
    imgs[currentImageIndex].classList.add('active');
  }, 5000);
}

document.addEventListener('DOMContentLoaded', initCarousel);
