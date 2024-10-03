const taskForm = document.getElementById('add-task');
const newTaskBtn = taskForm.children['new-task-button'];
const taskText = taskForm.children['task-text'];

const selectTab = document.getElementById('select-tab');
const tabs = selectTab.children

const tasks = document.getElementById('tasks');

newTaskBtn.addEventListener('click', () =>{
    let taskCount = tasks.children.length;

    if (taskText.value) {
        const newTaskListItem = document.createElement('li');
        newTaskListItem.classList.add('list-group-item', 'rounded-3');
        newTaskListItem.id = `task${taskCount}`;

        // Task text
        // Para elementas reikalingas, nes negalim talpint teksto su input buttonu priesais teksta
        // Pabandzius perrasom elemento innerHTML'a ir prarandam input boxa;
        // Sprendimas gallimas su innerHTML papildymu, taciau tai leidzia inputint ir renderint htmla.
        const newTaskText = document.createElement('p');
        newTaskText.className = 'd-inline';
        newTaskText.textContent = taskText.value;

        const taskCbox = document.createElement('input');
        taskCbox.type = 'checkbox';
        taskCbox.name = 'done-task';
        taskCbox.className = 'me-2';
        
        newTaskListItem.appendChild(taskCbox);
        newTaskListItem.appendChild(newTaskText);
        tasks.append(newTaskListItem)
    
        taskText.value = '';
    }
});

