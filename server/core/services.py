# core/services.py
from django.db.models import Prefetch
from .models import UniversityGroup
from users.models import Account
from teams.models import Team
from projects.models import Project, Idea

class StudentsTableService:
    
    @staticmethod
    def get_students_hierarchy_debug():
        """Отладочная версия для выявления проблем"""
        
        print("🔍 Начинаем отладку...")
        
        # Проверяем, есть ли группы
        groups = UniversityGroup.objects.all()
        print(f"📊 Найдено групп: {groups.count()}")
        for group in groups:
            print(f"   - {group.name} ({group.institute})")
        
        # Проверяем, есть ли пользователи с группами
        users_with_groups = Account.objects.filter(university_group__isnull=False)
        print(f"👥 Пользователей с группами: {users_with_groups.count()}")
        for user in users_with_groups:
            print(f"   - {user.first_name} {user.last_name} -> {user.university_group}")
        
        # Проверяем команды
        teams = Team.objects.all()
        print(f"🏢 Всего команд: {teams.count()}")
        for team in teams:
            print(f"   - {team.name} (статус: {team.status}, участников: {team.members.count()})")
        
        # Проверяем проекты и идеи
        projects = Project.objects.all()
        ideas = Idea.objects.all()
        print(f"📋 Проектов: {projects.count()}, Идей: {ideas.count()}")
        
        # Основная логика без фильтров
        institutes_dict = {}
        
        for user in users_with_groups:
            print(f"\n🔍 Обрабатываем пользователя: {user.first_name} {user.last_name}")
            
            # Получаем ВСЕ команды пользователя (без фильтров)
            user_teams = user.teams.all()
            print(f"   Команд пользователя: {user_teams.count()}")
            
            teams_data = []
            for team in user_teams:
                print(f"   🏢 Команда: {team.name}")
                
                # Получаем ВСЕ проекты и идеи (без фильтров статуса)
                all_projects = team.projects.all()
                all_ideas = team.ideas.all()
                print(f"      Проектов: {all_projects.count()}, Идей: {all_ideas.count()}")
                
                projects_ideas_data = []
                
                # Добавляем все проекты
                for project in all_projects:
                    print(f"         📋 Проект: {project.title} (статус: {project.status})")
                    projects_ideas_data.append({
                        'id': project.id,
                        'title': project.title,
                        'type': 'project',
                        'status': project.status
                    })
                
                # Добавляем все идеи
                for idea in all_ideas:
                    print(f"         💡 Идея: {idea.title} (статус: {idea.status})")
                    projects_ideas_data.append({
                        'id': idea.id,
                        'title': idea.title,
                        'type': 'idea',
                        'status': idea.status
                    })
                
                # Добавляем команду даже если нет проектов/идей
                teams_data.append({
                    'id': team.id,
                    'name': team.name,
                    'projects_or_ideas': projects_ideas_data
                })
            
            # Добавляем пользователя даже если нет команд
            group = user.university_group
            institute_code = group.institute
            institute_name = group.get_institute_display()
            
            if institute_code not in institutes_dict:
                institutes_dict[institute_code] = {
                    'institute_code': institute_code,
                    'institute_name': institute_name,
                    'groups': {}
                }
            
            if group.name not in institutes_dict[institute_code]['groups']:
                institutes_dict[institute_code]['groups'][group.name] = {
                    'group_id': group.id,
                    'group_name': group.name,
                    'users': []
                }
            
            institutes_dict[institute_code]['groups'][group.name]['users'].append({
                'id': user.id,
                'full_name': f"{user.first_name} {user.last_name}".strip(),
                'email': user.email,
                'teams': teams_data,
                'avatar': user.avatar.url if user.avatar else None,
            })
        
        # Преобразуем в финальную структуру
        institutes_data = []
        for institute in institutes_dict.values():
            institute['groups'] = list(institute['groups'].values())
            institutes_data.append(institute)
        
        print(f"\n✅ Финальный результат: {len(institutes_data)} институтов")
        return institutes_data