<template>
  <div>
    <Header/>
    <div class="w-4/5 mt-5 m-auto p-6 overflow-auto flex gap-3 items-start z-10">
      <button
        @click="goBack"
        :style="{ backgroundColor: currentBgColor }"
        class="ml-auto font-medium rounded-lg text-sm px-4 py-2 mt-5 duration-300 h-10 w-14 items-center"
      >
        <svg
          width="20"
          height="25"
          viewBox="0 0 12 12"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M5.27934 8.23871C5.35303 8.30737 5.41213 8.39017 5.45312 8.48217C5.49411 8.57417 5.51616 8.67348 5.51793 8.77418C5.51971 8.87489 5.50118 8.97492 5.46346 9.0683C5.42574 9.16169 5.3696 9.24653 5.29838 9.31774C5.22716 9.38896 5.14233 9.44511 5.04894 9.48283C4.95555 9.52055 4.85552 9.53907 4.75482 9.5373C4.65412 9.53552 4.5548 9.51348 4.4628 9.47249C4.3708 9.4315 4.288 9.37239 4.21934 9.29871L0.21934 5.29871C0.0788892 5.15808 -1.99759e-07 4.96746 -2.08447e-07 4.76871C-2.17135e-07 4.56996 0.0788892 4.37933 0.21934 4.23871L4.21934 0.238705C4.288 0.165019 4.3708 0.105917 4.4628 0.064925C4.5548 0.023933 4.65411 0.00189198 4.75482 0.000115187C4.85552 -0.0016616 4.95555 0.0168623 5.04894 0.0545833C5.14233 0.0923043 5.22716 0.148449 5.29838 0.219668C5.3696 0.290887 5.42574 0.375721 5.46346 0.469109C5.50118 0.562497 5.51971 0.662525 5.51793 0.763228C5.51615 0.863931 5.49411 0.963245 5.45312 1.05524C5.41213 1.14724 5.35303 1.23004 5.27934 1.29871L2.55934 4.01871L12.2493 4.01871C12.4483 4.01871 12.639 4.09772 12.7797 4.23838C12.9203 4.37903 12.9993 4.56979 12.9993 4.76871C12.9993 4.96762 12.9203 5.15838 12.7797 5.29904C12.639 5.43969 12.4483 5.51871 12.2493 5.51871L2.55934 5.51871L5.27934 8.23871Z"
            fill="white"
          />
        </svg>
      </button>

<!-- Контейнер для вертикальных блоков (увеличенная ширина) -->
<div class="flex flex-col gap-6">
  
  <!-- Контейнер с информацией о команде (увеличенная ширина) -->
  <div class="w-full bg-card rounded-lg p-6 flex flex-col mt-5" style="height: 300px;">
    <div class="flex-grow overflow-auto">
      <h2 v-if="!isEditing" class="text-2xl font-semibold mb-4">{{ team.name || "Загрузка..." }}</h2>
      <input
        v-else
        v-model="editedTeam.name"
        class="w-full text-2xl bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none"
      />
      <h3 class="text-xl font-semibold mb-5">
        Тим-лид: {{ team.owner_name || "Неизвестный автор" }}
      </h3>
      <span
        class="bg-gray-200 mt-5 text-gray-700 px-2 py-1 rounded-full"
        :style="{ backgroundColor: statusStyleMap[team.status]?.bg || '#eee' }"
      >
        {{ statusStyleMap[team.status]?.label || team.status }}
      </span>
    </div>

    <!-- Блок с иконками прижат к низу -->
    <div class="mt-auto flex justify-end gap-5">
      <img @click="toggleEditing" class="w-6 h-6 cursor-pointer" :src="isDarkTheme ? '/pencil_light.svg' :'/pencil_dark.svg'"/>
      <button
        v-if="isEditing"
        @click="saveAllChanges"
        class="w-6 h-6 cursor-pointer"
      >
        <svg width="23" height="23" viewBox="0 0 12 9" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M11.7 0.7C11.3134 0.3134 10.6866 0.313401 10.3 0.7L4.2 6.8L2.1 4.7C1.7134 4.3134 1.0866 4.3134 0.7 4.7V4.7C0.313401 5.0866 0.3134 5.7134 0.699999 6.1L2.78579 8.18579C3.56683 8.96683 4.83316 8.96683 5.61421 8.18579L11.7 2.1C12.0866 1.7134 12.0866 1.0866 11.7 0.7V0.7Z" :fill="pathFillColor"/>
        </svg>
      </button>
      <button @click="showConfirmModal = true" class="h-6 w-6">
        <svg width="20" height="20" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5.5 1H8.5C8.63261 1 8.75979 1.05268 8.85355 1.14645C8.94732 1.24021 9 1.36739 9 1.5V2.5H5V1.5C5 1.36739 5.05268 1.24021 5.14645 1.14645C5.24021 1.05268 5.36739 1 5.5 1ZM10 2.5V1.5C10 1.10218 9.84196 0.720644 9.56066 0.43934C9.27936 0.158035 8.89782 0 8.5 0L5.5 0C5.10218 0 4.72064 0.158035 4.43934 0.43934C4.15804 0.720644 4 1.10218 4 1.5V2.5H0.5C0.367392 2.5 0.240215 2.55268 0.146447 2.64645C0.0526784 2.74021 0 2.86739 0 3C0 3.13261 0.0526784 3.25979 0.146447 3.35355C0.240215 3.44732 0.367392 3.5 0.5 3.5H1.038L1.891 14.16C1.93122 14.6612 2.15875 15.1289 2.52827 15.4698C2.8978 15.8108 3.38219 16.0001 3.885 16H10.115C10.6178 16.0001 11.1022 15.8108 11.4717 15.4698C11.8412 15.1289 12.0688 14.6612 12.109 14.16L12.962 3.5H13.5C13.6326 3.5 13.7598 3.44732 13.8536 3.35355C13.9473 3.25979 14 3.13261 14 3C14 2.86739 13.9473 2.74021 13.8536 2.64645C13.7598 2.55268 13.6326 2.5 13.5 2.5H10ZM11.958 3.5L11.112 14.08C11.0919 14.3306 10.9781 14.5644 10.7934 14.7349C10.6086 14.9054 10.3664 15.0001 10.115 15H3.885C3.6336 15.0001 3.3914 14.9054 3.20664 14.7349C3.02188 14.5644 2.90811 14.3306 2.888 14.08L2.042 3.5H11.958ZM4.471 4.5C4.60333 4.49235 4.73329 4.53756 4.8323 4.6257C4.93131 4.71383 4.99127 4.83767 4.999 4.97L5.499 13.47C5.50425 13.6008 5.45802 13.7284 5.37022 13.8255C5.28242 13.9225 5.16006 13.9813 5.02941 13.9892C4.89876 13.997 4.77024 13.9533 4.67144 13.8675C4.57265 13.7816 4.51145 13.6605 4.501 13.53L4 5.03C3.99594 4.96431 4.00489 4.89847 4.02633 4.83625C4.04777 4.77403 4.08129 4.71665 4.12495 4.66741C4.16862 4.61817 4.22158 4.57804 4.28079 4.54931C4.34 4.52058 4.4043 4.50382 4.47 4.5H4.471ZM9.529 4.5C9.5947 4.50382 9.659 4.52058 9.71821 4.54931C9.77742 4.57804 9.83038 4.61817 9.87405 4.66741C9.91771 4.71665 9.95123 4.77403 9.97267 4.83625C9.99411 4.89847 10.0031 4.96431 9.999 5.03L9.499 13.53C9.49633 13.5964 9.48043 13.6617 9.45224 13.7219C9.42405 13.7821 9.38413 13.8361 9.33481 13.8807C9.28549 13.9254 9.22777 13.9597 9.16503 13.9817C9.10228 14.0037 9.03578 14.013 8.9694 14.009C8.90302 14.005 8.8381 13.9878 8.77845 13.9585C8.7188 13.9291 8.6656 13.8881 8.62199 13.8379C8.57837 13.7877 8.5452 13.7293 8.52443 13.6661C8.50365 13.603 8.49569 13.5363 8.501 13.47L9.001 4.97C9.00873 4.83767 9.06869 4.71383 9.1677 4.6257C9.26671 4.53756 9.39667 4.49235 9.529 4.5ZM7 4.5C7.13261 4.5 7.25979 4.55268 7.35355 4.64645C7.44732 4.74021 7.5 4.86739 7.5 5V13.5C7.5 13.6326 7.44732 13.7598 7.35355 13.8536C7.25979 13.9473 7.13261 14 7 14C6.86739 14 6.74021 13.9473 6.64645 13.8536C6.55268 13.7598 6.5 13.6326 6.5 13.5V5C6.5 4.86739 6.55268 4.74021 6.64645 4.64645C6.74021 4.55268 6.86739 4.5 7 4.5Z" :fill="pathFillColor"/>
        </svg>
      </button>



    </div>
  </div>

  <!-- Контейнер с кнопками (увеличенная ширина) -->
  <div class="w-full rounded-lg flex flex-col gap-2">
    <button
      @click="sendJoinRequest"
      :style="{ backgroundColor: currentBgColor }"
      @mouseover="currentBgColor = instituteStyle.buttonOnColor"
      @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      class="text-always-white inline-flex items-center justify-center focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full"
    >
      <svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
      </svg>
      Присоединиться
    </button>

    <button
      @click="openModal"
      :style="{ backgroundColor: currentBgColor }"
      @mouseover="currentBgColor = instituteStyle.buttonOnColor"
      @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      class="text-always-white inline-flex items-center justify-center focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full"
    >
      Посмотреть заявки
    </button>

    <button
      :style="{ backgroundColor: currentBgColor }"
      @mouseover="currentBgColor = instituteStyle.buttonOnColor"
      @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
      @click="showIdeaModal"
      class="text-always-white inline-flex items-center justify-center focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center w-full"
    >
      Создать идею в рамках команды
    </button>
  </div>
</div>


    <div class="w-2/4 mt-5 bg-card rounded-lg p-6 overflow-auto"  style="height: auto; max-height: 100vh; overflow-y: auto;">
      <h2 class="text-2xl font-semibold mb-4">Описание идеи</h2>
  <div v-if="isEditing">
          <label for="status" class="font-semibold mb-3">Изменить статус:</label>
          <select
            id="status"
            v-model="editedTeam.status"
            @change="updateStatus"
            class="w-full bg-input rounded-md p-2 mt-3 mb-3"
          >
            <option value="in_process">В работе</option>
            <option value="open">Открытый</option>
            <option value="private">Закрытый</option>
          </select>
        </div>
        <p v-if="!isEditing" class="opacity-70">
          {{ team.description }}
        </p>
        <textarea
          v-else
          v-model="editedTeam.description"
          class="w-full bg-input rounded-md p-2 focus:outline-none focus:ring-0 focus:border-none"
        ></textarea>


  <table class="w-full border-collapse shadow-lg rounded-lg overflow-hidden mt-5">
  <thead class="bg-input">
    <tr>
  <th class="p-3 text-left w-1/4">Имя участника</th>
  <th class="p-3 text-left w-2/6">Навыки</th>
  <th class="p-3 text-left w-1/9">Оценка</th>
  <th class="p-3 w-1/8">
    <img 
    @click="showAddMemberModal = true"
      width="30" 
      height="30" 
      :src="imageSrc"
      alt="add" 
      :class="{'dark-filter': isDarkTheme}" 
      style="float: right;"
    />
  </th>
</tr>
  </thead>
  <tbody>
    <tr v-for="member in team.members" :key="member.id" class="transition-colors ">
      <td class="p-3 border-t bg-card">
        {{ member.full_name }}
      </td>
      <td class="p-3 border-t bg-card">
  <!-- Проверяем, есть ли у пользователя навыки -->
  <div>
    <template v-if="member.skills.length > 4">
      <!-- Отображаем первые 4 навыка и добавляем знак "+" с количеством оставшихся -->
      {{ member.skills.slice(0, 4).map(skillId => getSkillName(skillId)).join(", ") }}
      <span> +{{ member.skills.length - 4 }} </span> <!-- Количество оставшихся навыков -->
    </template>
    <template v-else>
      <!-- Если навыков 4 или меньше, выводим их все -->
      {{ member.skills.length ? member.skills.map(skillId => getSkillName(skillId)).join(", ") : "Нет навыков" }}
    </template>
  </div>
</td>
      <td class="p-3 border-t bg-card">{{ member.total_rating }}</td>
      <td class="p-3 border-t bg-card">
        <button @click="removeMember(member.id)" class="px-1 py-2 rounded-md transition-all transform hover:scale-105 ml- cursor-pointer" style="float: right;"
        >
          ❌
        </button>
      </td>
    </tr>
  </tbody>
</table>


    </div>
   <div class="w-1/4 mt-5 bg-card rounded-lg p-6 flex flex-col z-content" style="height: 300px;">
  <div v-if="!isLoading" class="flex flex-col flex-grow">
    <!-- Проекты -->
    <div v-if="projects.length > 0">
      <h3 class="text-2xl font-semibold mb-1">Проекты</h3>
      <div v-for="project in projects" :key="project.id" class="widget-item" @click="goToProject(project.id)">
        <div class="widget-title font-semibold text-xl mb-1">{{ project.title }}</div>
        <div class="widget-title opacity-70 mb-4 truncate-text">{{ project.description }}</div>
      </div>
    </div>

    <!-- Идеи -->
    <div v-if="ideas.length > 0">
      <h3 class="text-2xl font-semibold mb-1">Идеи</h3>
      <div v-for="idea in ideas" :key="idea.id" class="widget-item" @click="goToIdea(idea.id)">
        <div class="widget-title text-xl">{{ idea.title }}</div>
      </div>
    </div>
  </div>

  <!-- Кнопка для перехода к активному элементу (проекту или идее) -->
  <div v-if="activeItemType && activeItemId" class="mt-auto">
    <button 
      @click="goToItem" 
      class="p-2 bg-black text-white rounded-lg mx-auto"
      style="background-color: rgba(0, 0, 0, 0.1); text-align: center; width: 200px;">
      Перейти к {{ activeItemType === 'project' ? 'проекту' : 'идее' }}
    </button>
  </div>

</div>
    </div>
<!-- Модальное окно для приватной команды -->
    <div v-if="isPrivate && showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-60">
      <div class="bg-card rounded-xl p-6 max-w-md w-full mx-4 shadow-2xl">
        <!-- Иконка и заголовок -->
        <div class="text-center mb-6">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
            <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Вы точно готовы начать работу?</h3>
        </div>

        <!-- Текст сообщения -->
        <div class="mb-6 text-center">
          <p class="text-gray-600">
            После создания идеи ваша команда автоматически начнёт работу над проектом и не сможет отправлять приглашения на проекты в бирже проектов.
          </p>
        </div>

        <!-- Кнопки действий -->
        <div class="flex justify-center space-x-4">
          <button @click="closeIdeaModal" class="px-5 py-2.5 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            Назад
          </button>
          <button @click="openCreateIdeaModal" class="px-5 py-2.5 text-always-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200">
            Создать
          </button>
        </div>


      </div>        

    
        </div>

<RespondedTeams
      v-if="isModalOpen"
      :teamId="teamId"
      @close="closeModal"
    />
      <IdeaCreateModal
  :show="showCreateIdeaModal"
  :teamId="teamId"
  @close="closeCreateIdeaModal"
  @created="onIdeaCreated"
/>



<div class="w-4/5 mx-auto">
    <!-- Кнопка -->
    <button
      @click="toggleKanban"
      class="w-full  text-always-white font-semibold py-4 px-6 rounded-t-lg shadow-lg transition-colors duration-200 flex items-center justify-center relative z-10"
      :class="{ 'rounded-b-none': isOpen, 'rounded-b-lg': !isOpen }"
      :style="{ backgroundColor: currentBgColor }"
      @mouseover="currentBgColor = instituteStyle.buttonOnColor"
      @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
    >
      <span class="text-lg">{{ isOpen ? 'Скрыть канбан-доску' : 'Открыть канбан-доску' }}</span>
      <svg
        :class="{ 'rotate-180': isOpen }"
        class="ml-2 w-5 h-5 transition-transform duration-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Контейнер с фиксированной высотой -->
    <div
      class="bg-gray-100 border border-gray-200 border-t-0 rounded-b-lg shadow-lg overflow-hidden transition-all duration-600 ease-out z-1"
      :style="{ 
        height: isOpen ? '800px' : '0px',
        opacity: isOpen ? 1 : 0,
        transform: isOpen ? 'scaleY(1)' : 'scaleY(0)',
        transformOrigin: 'top'
      }"
    >
      <div class="p-6 h-full">
        <Kanban :teamId="teamId" />
      </div>
    </div>
  </div>



  <!-- Модальное окно для команды, не имеющей статус "приватный" -->
    <div v-if="!isPrivate && showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-60">
      <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-2xl">
        <!-- Иконка и заголовок -->
        <div class="text-center mb-6">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
            <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Сначала сделайте команду приватной</h3>
        </div>

        <!-- Текст сообщения -->
        <div class="mb-6 text-center">
          <p class="text-gray-600">
            Вы не можете создать идею, так как ваша команда не имеет статус приватности. Измените статус команды и вы сможете создать идею.
          </p>
        </div>

        <!-- Кнопка действия -->
        <div class="flex justify-center">
          <button @click="closeIdeaModal" class="px-5 py-2.5 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            Назад
          </button>
        </div>
      </div>
    </div>
      <!-- Модалка подтверждения -->
    <TeamDeleteModal
      :show="showConfirmModal"
      :teamId="teamId"
      @close="closeConfirmModal"
      @delete="handleDeleteTeam"
      @disband="handleDisbandTeam"
    />
<!-- Модальное окно -->
    <div v-if="showAddMemberModal" class="fixed inset-0 flex justify-center items-center z-70">
      <div class="bg-card rounded-lg p-6 max-w-sm w-full z-70">
        <h2 class="text-xl font-semibold mb-4 ">Добавить участника</h2>

        <!-- Поле ввода для ID пользователя -->
        <div class="mb-4">
          <label for="userId" class="block text-sm font-medium text-gray-700">Введите ID пользователя:</label>
          <input 
            id="userId" 
            v-model="user_Id" 
            type="text" 
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-input"
            placeholder="ID пользователя"
          />
        </div>

        <!-- Кнопки -->
        <div class="flex justify-between">
          <button 
            @click="addMember"
            :style="{ backgroundColor: currentBgColor }"
        @mouseover="currentBgColor = instituteStyle.buttonOnColor"
        @mouseleave="currentBgColor = instituteStyle.buttonOffColor"
            class="px-4 py-2  text-always-white rounded-lg ">
            Добавить
          </button>
          <button 
            @click="closeMemberModal"
            class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400">
            Отмена
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/composables/auth.js"; // axios-инстанс с интерсепторами
import Header from "@/components/header.vue";
import Kanban from "@/components/teams/board.vue";
import Cookies from "js-cookie"; 
import { deleteTeam, disbandTeam  } from "@/services/teamService";
import { instituteStyles } from "@/assets/instituteStyles.js";
import RespondedTeams from "@/components/teams/request.vue";
import IdeaCreateModal from "@/components/teams/createIdea.vue";
import TeamDeleteModal from "@/components/teams/TeamDeleteModal.vue";

export default {
  inject: ["globalState"],
  name: "TeamDetails",
  components: {
    Header, RespondedTeams, Kanban, IdeaCreateModal, TeamDeleteModal
  },
  props: {
    institute: {
      type: String,
      required: false,
    },
    teamId: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      showAddMemberModal: false,
      imageSrc: 'https://img.icons8.com/sf-regular/48/add.png',
      statusStyleMap: this.getStatusStyleMap(),
      showCreateIdeaModal: false,
      showModal: false,
      isPrivate: false,
      projects: [],
      ideas: [],
      isLoading: false,
      activeItemType: null,  // Поле для хранения активного типа (project или idea)
      activeItemId: null,
      members: [],
      isModalOpen: false,
      currentBgColor: "",
      userData: null,
      showConfirmModal: false,
      userId: null,
      user_Id: '',
      team: {},                // Объект с данными команды
      isEditing: false,        // Флаг режима редактирования
      editedTeam: {            // Копия данных для редактирования
        name: "",
        description: "",
        status: "",
      },
      errorMessage: '',        // Сообщения об ошибках
      skills: [],
      isOpen: false
    };
  },
  computed: {
    isDarkTheme() {
    if (!this.userData) return false;
    return this.userData.mode === 'dark';
  },
  pathFillColor() {
      return this.isDarkTheme ? "white" : "black";
    },
    selectedInstitute() {
      return this.globalState.institute;
    },
    instituteStyle() {
      const style = instituteStyles[this.selectedInstitute];
      return style || { buttonOffColor: "#ccc" };
    },
    /**
     * Получает данные текущего пользователя из Cookies.
     */
    currentUser() {
      return JSON.parse(localStorage.getItem("userData") || "{}");
    },
    /**
     * Определяет, является ли текущий пользователь владельцем команды.
     */
    isOwner() {
      return this.team.owner === this.currentUser;
    },
    /**
     * Для простоты: права редактирования доступны только владельцу.
     */
    hasEditAccess() {
      return this.isOwner;
    },
  },
  watch: {
    teamId: {
      immediate: true,
      handler(newId) {
        console.log("Получен новый teamId:", newId);
        if (newId) {
          this.fetchTeamDetails(newId);
        }
      },
    },
    instituteStyle: {
      handler(newStyle) {
        this.currentBgColor = newStyle.buttonOffColor;
      },
      immediate: true,
    },
  },
  async mounted() {
    try {
    const response = await api.get(`/teams/${this.teamId}/`);  // Запрос на сервер для получения данных о команде
    this.isPrivate = ['private', 'Приватная'].includes(response.data.status);
    console.log('isPrivate установлен в:', this.isPrivate);
  } catch (error) {
    console.error('Ошибка загрузки данных команды', error);
  }
    await this.loadBoardOptions();
    this.currentBgColor = this.instituteStyle.buttonOffColor;
    const userData = JSON.parse(localStorage.getItem('userData'));
    console.log('teamId:', this.teamId, 'Тип данных:', typeof this.teamId);
    this.userId = userData?.id;
    this.loadTechnologies();
  },
  methods: {
    toggleKanban() {
      this.isOpen = !this.isOpen
    },
    openCreateIdeaModal() {
    this.showModal = false; // Закрываем первую модалку
    this.showCreateIdeaModal = true; // Открываем модалку создания идеи
  },
  
  closeCreateIdeaModal() {
    this.showCreateIdeaModal = false; // Закрываем модалку создания идеи
  },
  
  onIdeaCreated(ideaData) {
    console.log('Идея создана:', ideaData);
    this.showCreateIdeaModal = false;
    this.$toast?.success?.('Идея успешно создана!');
  },
    closeMemberModal() {
      this.showAddMemberModal = false;
      this.user_Id = ''; // Сбросить введенное значение
    },
    
    // Метод для добавления участника
    async addMember() {
      if (!this.user_Id) {
        alert('Пожалуйста, введите ID пользователя');
        return;
      }
      
      try {
        // Тут можно вызвать API для добавления пользователя по его ID
        const response = await api.post(`/teams/${this.teamId}/add_member/`, {
          user_id: this.user_Id,
        });

        alert('Пользователь добавлен в команду');
        this.closeMemberModal(); // Закрыть модалку после добавления
      } catch (error) {
        console.error('Ошибка при добавлении пользователя:', error);
        alert('Не удалось добавить участника');
      }
    },
    getStatusStyleMap() {
      return {
        Приватная: { label: "Приватная", bg: "#fff3cd" },
        Открытая: { label: "Открытая", bg: "#d4edda" },
        Распалась: { label: "Распалась", bg: "#e2e3e5" },
        В_работе: { label: "В работе", bg: "#A1FFB7" },
      };
    },
    showIdeaModal() {
  this.showModal = true;
},
    // Закрыть модальное окно
    closeIdeaModal() {
      this.showModal = false;
    },
    async loadBoardOptions() {
    this.isLoading = true;
    try {
      const response = await api.get(`/teams/${this.teamId}/board_options/`);
      this.projects = response.data.projects || [];
      this.ideas = response.data.ideas || [];

      // Пример: Определим, над чем работает команда (проект или идея)
      if (this.projects.length > 0) {
        this.activeItemType = 'project';
        this.activeItemId = this.projects[0].id;  // Выбираем первый проект как активный
      } else if (this.ideas.length > 0) {
        this.activeItemType = 'idea';
        this.activeItemId = this.ideas[0].id;  // Выбираем первую идею как активную
      }

    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    } finally {
      this.isLoading = false;
    }
  },
  goToItem() {
  const institute = this.globalState.institute; // Получаем значение из глобального состояния
  let url = '';

  if (this.activeItemType === 'project' && this.activeItemId) {
    // Формируем ссылку для проекта
    url = `/${institute}/project/${this.activeItemId}`;
  } else if (this.activeItemType === 'idea' && this.activeItemId) {
    // Формируем ссылку для идеи
    url = `/${institute}/idea/${this.activeItemId}`;
  }

  if (url) {
    // Переходим на сформированный URL
    this.$router.push(url);
  }
},
    async loadTechnologies() {
      try {
        const response = await api.get('/core/technologies');
        this.skills = response.data; // Сохраняем полученные скиллы в массив
      } catch (error) {
        console.error('Ошибка при загрузке скиллов:', error);
      }
    },
    // Получаем название скилла по ID
    getSkillName(skillId) {
      const skill = this.skills.find(tech => tech.id === skillId);
      return skill ? skill.name : 'Неизвестный скилл'; // Если скилл найден, возвращаем его название
    },
    async removeMember(userId) {
      try {
        // Попросим сервер удалить участника по его ID
        const response = await api.post(`/teams/${this.team.id}/remove_member/`, {
          user_id: userId,
        });
        
        // Если удаление прошло успешно, удалим участника из списка
        const index = this.team.members.findIndex(member => member.id === userId);
        if (index !== -1) {
          this.team.members.splice(index, 1); // Удаляем участника из списка
        }
        
        alert('Пользователь удален из команды');
      } catch (error) {
        console.error("Ошибка при удалении участника:", error);
        alert('Не удалось удалить участника');
      }
    },

    closeConfirmModal() {
      this.showConfirmModal = false;
    },

    async handleDeleteTeam() {
      try {
        // Вызываем метод из teams.js
        await deleteTeam(this.teamId);
        
        this.showConfirmModal = false;
        this.$toast?.success?.('Команда успешно удалена!') || 
        alert('Команда успешно удалена!');
        
        // Перенаправление
        this.$router.go(-1);
        
      } catch (error) {
        console.error("Ошибка при удалении команды:", error.response?.data || error);
        this.$toast?.error?.('Не удалось удалить команду. Попробуйте позже.') ||
        alert('Не удалось удалить команду. Попробуйте позже.');
      }
    },
    // Распуск команды (остается в истории)
    async handleDisbandTeam() {
      try {
        const response = await api.post(`/teams/${this.teamId}/disband/`);
        
        console.log('Команда распущена:', response.data);
        
        this.showConfirmModal = false;
        this.$toast?.success?.('Команда успешно расформирована!') ||
        alert('Команда успешно расформирована!');
        
        // Обновляем данные команды или перенаправляем
        this.$router.go(-1);
        
      } catch (error) {
        console.error("Ошибка при расформировании команды:", error.response?.data || error);
        
        let errorMessage = 'Не удалось расформировать команду';
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }
        
        this.$toast?.error?.(errorMessage) ||
        alert(errorMessage);
      }
    },
  async sendJoinRequest() {
    try {
      // 1) парсим ID команды
      const teamId = parseInt(this.teamId, 10);
      if (isNaN(teamId)) {
        console.error("teamId должен быть целым числом");
        return;
      } 

      // 2) создаём заявку на вступление
      const requestData = {
        team: teamId,
        message: "Хочу присоединиться к вашей команде!",
      };
      console.log("Заявка отправлена:", requestData);
      const { data: joinReq } = await api.post("/team-join-requests/", requestData);
      console.log("Заявка отправлена:", joinReq);

    } catch (error) {
      console.error("Ошибка при отправке заявки или уведомления:", error.response || error);
      this.errorMessage = "Не удалось отправить заявку или уведомление.";
    }
  },
    /**
     * Перенаправляет пользователя на предыдущую страницу.
     */
    goBack() {
      this.$router.go(-1);
    },
    /**
     * Обновляет данные команды через API с использованием настроенного axios-инстанса.
     */
    async fetchTeamDetails(teamId) {
      try {
        // Используем инстанс api – он сам позаботится о токене
        const response = await api.get(`/teams/${teamId}/`);
        if (response.status !== 200) {
          throw new Error(`Ошибка загрузки команды: ${response.status}`);
        }
        this.team = response.data;
        console.log("Данные команды получены:", this.team);
      } catch (error) {
        console.error("Ошибка при получении данных команды:", error.response?.data || error);
      }
    },
    /**
     * Переключает режим редактирования команды.
     * Если включён режим редактирования, копирует текущие данные команды в editedTeam.
     */
    toggleEditing() {
      this.isEditing = !this.isEditing;
      if (this.isEditing) {
        this.editedTeam = {
          name: this.team.name,
          description: this.team.description,
          status: this.team.status || "",
        };
      }
    },
    /**
     * Сохраняет изменения в команде через API.
     */
    async saveAllChanges() {
      try {
        const payload = {
          ...(this.editedTeam.name && { name: this.editedTeam.name }),
          ...(this.editedTeam.description && { description: this.editedTeam.description }),
          status: this.editedTeam.status || null,
        };
        console.log("Payload перед сохранением:", payload);
        const response = await api.put(`/teams/${this.team.id}/`, payload, {
          headers: { "Content-Type": "application/json" },
        });
        console.log("Изменения сохранены:", response.data);
        // Обновляем данные команды после сохранения
        await this.fetchTeamDetails(this.team.id);
      } catch (error) {
        console.error("Ошибка при сохранении изменений:", error.response?.data || error);
      }
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
  },
};
</script>

<style scoped>
.flex-col {
  display: flex;
  flex-direction: column;
}
.image-container {
  display: table-cell; /* Ячейка таблицы */
  text-align: center; /* Центрирование по горизонтали */
  vertical-align: middle; /* Центрирование по вертикали */
  width: 100%; /* Убедитесь, что контейнер занимает всю ширину ячейки */
}
.z-60 {
  z-index: 60; /* Обеспечим, чтобы модалки были выше колонок */
}
.z-70 {
  z-index: 70; /* Обеспечим, чтобы модалки были выше колонок */
}
.fixed {
  background: rgba(0, 0, 0, 0.3); /* Полупрозрачный черный */
  backdrop-filter: blur(5px); /* Эффект размытия */
}
.dark-filter {
  filter: invert(1);
}
.truncate-text {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
}
.z-content {
  z-index: 1 !important;
}
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.5s ease-in-out;
}

.slide-down-enter-from {
  height: 0;
  opacity: 0;
}

.slide-down-leave-to {
  height: 0;
  opacity: 0;
}
</style>
