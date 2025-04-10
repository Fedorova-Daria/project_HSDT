<template>
    <!-- Размытый фон с параллакс-эффектом -->
    <img
      ref="backgroundImage"
      class="absolute top-0 left-0 h-full w-full object-cover filter blur-md transform-gpu scale-105 -z-10"
      src="/bgg.jpg"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.05)`,
        transition: 'transform 0.5s cubic-bezier(0.13, 0.62, 0.23, 0.99)',
      }"
    />
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Параллакс-эффект
        offsetX: 0,
        offsetY: 0,
        targetX: 0,
        targetY: 0,
        mouseX: 0,
        mouseY: 0,
        windowWidth: 0,
        windowHeight: 0,
        animationFrame: null,
      };
    },
    methods: {
      // Инициализация параллакс-эффекта
      initParallax() {
        this.windowWidth = window.innerWidth;
        this.windowHeight = window.innerHeight;
        window.addEventListener("mousemove", this.handleMouseMove);
        window.addEventListener("resize", this.handleResize);
        this.animate();
      },
  
      handleMouseMove(e) {
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
  
        // Вычисляем смещение относительно центра экрана (от -1 до 1)
        const x = (e.clientX / this.windowWidth - 0.5) * 2;
        const y = (e.clientY / this.windowHeight - 0.5) * 2;
  
        // Устанавливаем целевые координаты с коэффициентом
        const coefficient = 30;
        this.targetX = x * coefficient;
        this.targetY = y * coefficient;
      },
  
      handleResize() {
        this.windowWidth = window.innerWidth;
        this.windowHeight = window.innerHeight;
      },
  
      animate() {
        // Интерполяция с коэффициентом плавности
        const smoothness = 0.08;
        this.offsetX += (this.targetX - this.offsetX) * smoothness;
        this.offsetY += (this.targetY - this.offsetY) * smoothness;
  
        this.animationFrame = requestAnimationFrame(this.animate);
      },
  
      cleanupParallax() {
        window.removeEventListener("mousemove", this.handleMouseMove);
        window.removeEventListener("resize", this.handleResize);
        if (this.animationFrame) {
          cancelAnimationFrame(this.animationFrame);
        }
      },
    },
    mounted() {
      this.initParallax();
    },
    beforeDestroy() {
      this.cleanupParallax();
    },
  };
  </script>
  
  <style scoped>
  /* Стили для параллакс-эффекта */
  .transform-gpu {
    transform: translateZ(0);
    backface-visibility: hidden;
    perspective: 1000px;
  }
  
  .filter {
    filter: blur(8px);
  }
  </style>