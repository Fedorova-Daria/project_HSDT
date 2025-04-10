<template>
    <div>
         <Header />
    <div class="page-container">
     
      <div class="content-wrapper">
        <!-- Обновлённый боковой блок -->
        <div class="sidebar">
          <div class="platform-info">
            <h3><span class="icon">ℹ️</span> О платформе</h3>
            <div class="platform-feature">
              <div class="feature-icon">👥</div>
              <div class="feature-text">Для студентов и сотрудников ТИУ</div>
            </div>
            <div class="platform-feature">
              <div class="feature-icon">💡</div>
              <div class="feature-text">Предложение идей</div>
            </div>
            <div class="platform-feature">
              <div class="feature-icon">👋</div>
              <div class="feature-text">Поиск единомышленников</div>
            </div>
            <div class="platform-feature">
              <div class="feature-icon">🛠️</div>
              <div class="feature-text">Поддержка проектов</div>
            </div>
            <div class="platform-feature">
              <div class="feature-icon">🚀</div>
              <div class="feature-text">Реализация задумок</div>
            </div>
            <div class="platform-footer">
              ТИУ - территория возможностей!
            </div>
          </div>
        </div>
  
        <div class="main-content">
          <!-- Стилизованный заголовок -->
          <div class="main-title text-white">
            <span>ДАВАЙТЕ</span>
            <span>МЕНЯТЬ</span>
            <span class="highlight">ТИУ</span>
            <span>ВМЕСТЕ!</span>
          </div>
  
          <!-- Галерея фотографий -->
          <div class="gallery">
            <div class="gallery-item" v-for="(image, index) in universityImages" :key="index">
              <img :src="image.src" :alt="image.alt" />
              <p class="image-caption">{{ image.caption }}</p>
            </div>
          </div>
  
          <div class="info-block">
            Добро пожаловать на платформу идей студентов ТИУ!
          </div>
  
          <div class="description">
            <p>Мы создали этот сайт для студентов и сотрудников Тюменского индустриального университета, чтобы каждый мог предложить идею, найти единомышленников и довести свой проект до реализации. Здесь ваш голос будет услышан, а задумки — найдут поддержку!</p>
          </div>
  
          <button class="suggestion-button" @click="showModal = true">
            У меня есть предложение
          </button>
  
          <!-- Блоки возможностей -->
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">🏛️</div>
              <h3>Выбор института</h3>
              <p>У нас несколько институтов: ВШЦТ, АРХИД, ИПТИ, СТРОИН. Каждый институт имеет свою уникальную страницу.</p>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">💡</div>
              <h3>Создание идеи</h3>
              <p>Опишите свою задумку, добавьте теги и начните получать отклики.</p>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">💬</div>
              <h3>Обсуждение</h3>
              <p>Оставляйте комментарии, улучшайте идеи вместе с сообществом.</p>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">🚀</div>
              <h3>Развитие проекта</h3>
              <p>Лучшие идеи могут перерасти в реальные студенческие инициативы!</p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Секция поддержки проектов -->
      <div class="project-support">
        <h3>Есть проект, но не хватает ресурсов?</h3>
        <p>Найдите поддержку среди студентов, преподавателей и администрации.</p>
        <button class="support-button" @click="showSupportModal = true">
          Найти поддержку
        </button>
      </div>
  
      <!-- Модальное окно предложения -->
      <div class="modal" v-if="showModal">
        <div class="modal-content">
          <span class="close" @click="showModal = false">&times;</span>
          <h3>Хотите улучшить университет?</h3>
          <p>Ваши предложения помогут изменить его к лучшему.</p>
          <button class="modal-button" @click="showModal = false">
            Поделиться идеей
          </button>
        </div>
      </div>
  
      <!-- Модальное окно поддержки -->
      <div class="modal" v-if="showSupportModal">
        <div class="modal-content">
          <span class="close" @click="showSupportModal = false">&times;</span>
          <h3>Поиск поддержки для проекта</h3>
          <p>Расскажите о своем проекте и нужных ресурсах.</p>
          <button class="modal-button" @click="showSupportModal = false">
            Отправить запрос
          </button>
        </div>
      </div>
  
      <!-- Плавающее облачко -->
      <div class="speech-bubble" :class="{ 'visible': showBubble }">
        <div class="bubble-content">
          <h3>Давайте менять ТИУ вместе!</h3>
          <p>Присоединяйтесь, публикуйте идеи и помогайте университету развиваться. Ваше мнение — это шаг к будущему!</p>
        </div>
        <button class="close-bubble" @click="showBubble = false">×</button>
      </div>
    </div>
</div>
  </template>
  
  <script>
  import Header from "@/components/header.vue"
  
  export default {
    components: {Header},
    data() {
      return {
        showModal: false,
        showSupportModal: false,
        showBubble: false,
        universityImages: [
          {
            src: "https://example.com/tiu-building1.jpg",
            alt: "Главный корпус ТИУ",
            caption: "Главный корпус ТИУ"
          },
          {
            src: "https://example.com/tiu-building2.jpg",
            alt: "Студенты в лаборатории",
            caption: "Современные лаборатории"
          },
          {
            src: "https://example.com/tiu-building3.jpg",
            alt: "Библиотека ТИУ",
            caption: "Научная библиотека"
          },
          {
            src: "https://example.com/tiu-building4.jpg",
            alt: "Студенческие мероприятия",
            caption: "Активная студенческая жизнь"
          }
        ]
      }
    },
    mounted() {
      setTimeout(() => {
        this.showBubble = true;
      }, 3000);
    }
  }
  </script>
  
  <style scoped>
  /* Основные стили */
  .page-container {
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
  }
  
  .content-wrapper {
    display: flex;
    gap: 30px;
    margin-top: 20px;
  }
  
  /* Стили для обновлённого бокового блока */
  .sidebar {
    width: 280px;
    background: linear-gradient(135deg, #f8f4ff 0%, #f0e6ff 100%);
    border-radius: 12px;
    padding: 0;
    box-shadow: 0 4px 12px rgba(138, 43, 226, 0.1);
    border: 1px solid #e8d6ff;
  }
  
  .platform-info {
    padding: 20px;
  }
  
  .platform-info h3 {
    color: #6a1b9a;
    font-size: 1.3rem;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e8d6ff;
    display: flex;
    align-items: center;
  }
  
  .platform-info h3 .icon {
    margin-right: 10px;
  }
  
  .platform-feature {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 8px;
    transition: all 0.3s ease;
  }
  
  .platform-feature:hover {
    background-color: rgba(138, 43, 226, 0.1);
    transform: translateX(5px);
  }
  
  .feature-icon {
    font-size: 1.5rem;
    margin-right: 12px;
    width: 30px;
    text-align: center;
    color: #8a2be2;
  }
  
  .feature-text {
    font-size: 0.95rem;
    color: #4a4a4a;
    font-weight: 500;
  }
  
  .platform-footer {
    margin-top: 25px;
    padding-top: 15px;
    border-top: 1px dashed #d1b3ff;
    font-size: 0.85rem;
    color: #8a2be2;
    text-align: center;
    font-style: italic;
  }
  
  /* Основной контент */
  .main-content {
    flex: 1;
  }
  
  /* Стили для заголовка */
  .main-title {
    font-family: 'Arial Black', sans-serif;
    font-size: 4rem;
    text-align: center;
    margin: 2rem 0;
    line-height: 1.2;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  
  .main-title span {
    display: block;
  }
  
  .main-title .highlight {
    color: #8a2be2;
    font-size: 5rem;
    text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
  }
  
  /* Галерея */
  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin: 40px 0;
  }
  
  .gallery-item {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  }
  
  .gallery-item:hover {
    transform: translateY(-5px);
  }
  
  .gallery-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
  }
  
  .image-caption {
    padding: 15px;
    text-align: center;
    background: white;
    margin: 0;
    font-weight: bold;
  }
  
  /* Инфо-блок */
  .info-block {
    background-color: #8a2be2;
    color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    margin: 20px 0;
    font-size: 1.2rem;
  }
  
  /* Описание */
  .description {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    line-height: 1.6;
    margin-bottom: 30px;
  }
  
  /* Кнопка предложения */
  .suggestion-button {
    background-color: #8a2be2;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: background-color 0.3s;
  }
  
  .suggestion-button:hover {
    background-color: #7b1fa2;
  }
  
  /* Блоки возможностей */
  .features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 40px;
  }
  
  .feature-card {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    border: 1px solid #e0e0e0;
  }
  
  .feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
  }
  
  .feature-card .feature-icon {
    font-size: 32px;
    margin-bottom: 15px;
    color: #8a2be2;
    width: auto;
  }
  
  .feature-card h3 {
    color: #8a2be2;
    margin-bottom: 10px;
  }
  
  .feature-card p {
    color: #555;
    line-height: 1.5;
    font-size: 14px;
  }
  
  /* Секция поддержки проектов */
  .project-support {
    background-color: #f0e6ff;
    padding: 30px;
    margin-top: 40px;
    border-radius: 8px;
    text-align: center;
    border-top: 3px solid #8a2be2;
  }
  
  .project-support h3 {
    color: #8a2be2;
    margin-bottom: 10px;
  }
  
  .project-support p {
    margin-bottom: 20px;
    color: #555;
  }
  
  .support-button {
    background-color: #8a2be2;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
  }
  
  .support-button:hover {
    background-color: #7b1fa2;
  }
  
  /* Модальные окна */
  .modal {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 30px;
    border-radius: 8px;
    width: 80%;
    max-width: 500px;
    position: relative;
    text-align: center;
  }
  
  .close {
    position: absolute;
    right: 15px;
    top: 10px;
    font-size: 24px;
    cursor: pointer;
  }
  
  .modal h3 {
    color: #8a2be2;
    margin-bottom: 15px;
  }
  
  .modal p {
    margin-bottom: 20px;
    font-size: 16px;
  }
  
  .modal-button {
    background-color: #8a2be2;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .modal-button:hover {
    background-color: #7b1fa2;
  }
  
  /* Плавающее облачко */
  .speech-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #8a2be2;
    color: white;
    border-radius: 15px;
    padding: 20px;
    width: 300px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.5s ease-out;
    z-index: 1000;
  }
  
  .speech-bubble.visible {
    transform: translateY(0);
    opacity: 1;
  }
  
  .speech-bubble::after {
    content: '';
    position: absolute;
    bottom: -10px;
    right: 40px;
    border-width: 10px 10px 0;
    border-style: solid;
    border-color: #8a2be2 transparent;
  }
  
  .bubble-content h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 18px;
  }
  
  .bubble-content p {
    margin: 0;
    font-size: 14px;
    line-height: 1.4;
  }
  
  .close-bubble {
    position: absolute;
    top: 5px;
    right: 10px;
    background: none;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
    padding: 0 5px;
  }
  
  .close-bubble:hover {
    color: #e0e0e0;
  }
  
  /* Адаптивность */
  @media (max-width: 1200px) {
    .features-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (max-width: 1024px) {
    .sidebar {
      width: 240px;
    }
    
    .main-title {
      font-size: 3rem;
    }
    
    .main-title .highlight {
      font-size: 4rem;
    }
  }
  
  @media (max-width: 768px) {
    .content-wrapper {
      flex-direction: column;
    }
    
    .sidebar {
      width: 100%;
      margin-bottom: 30px;
    }
    
    .features-grid {
      grid-template-columns: 1fr;
    }
    
    .main-title {
      font-size: 2.5rem;
    }
    
    .main-title .highlight {
      font-size: 3rem;
    }
  }
  
  @media (max-width: 600px) {
    .gallery {
      grid-template-columns: 1fr;
    }
    
    .speech-bubble {
      width: calc(100% - 40px);
      right: 20px;
      left: 20px;
    }
    
    .speech-bubble::after {
      right: 30px;
    }
    
    .main-title {
      font-size: 2rem;
    }
    
    .main-title .highlight {
      font-size: 2.5rem;
    }
  }
  </style>