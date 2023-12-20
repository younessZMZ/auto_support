document.addEventListener('DOMContentLoaded', function() {
    const taskContainer = document.getElementById('task-buttons');

    tasks.forEach(task => {
        const button = document.createElement('button');
        button.innerText = taskDescriptions[task];
        button.onclick = () => openTaskModal(task);
        taskContainer.appendChild(button);
    });
});

function openTaskModal(taskName) {
    const modal = document.getElementById('taskModal');
    const closeButton = document.querySelector('.close');
    const form = document.getElementById('taskForm');
    form.innerHTML = ''; // Clear existing form content

    const config = taskConfigs[taskName];

    // Create text inputs
    config.inputs.forEach(input => {
        const inputElement = document.createElement('input');
        inputElement.type = input.type;
        inputElement.name = input.name;
        inputElement.placeholder = input.placeholder;
        form.appendChild(inputElement);
    });

    // Create file input if required
    if (config.fileUpload) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.name = 'file';
        form.appendChild(fileInput);
    }

    // Add a hidden input to store the task name
    const taskNameInput = document.createElement('input');
    taskNameInput.type = 'hidden';
    taskNameInput.name = 'task';
    taskNameInput.value = taskName;
    form.appendChild(taskNameInput);

    // Add the submit button
    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.innerText = 'Run Task';
    form.appendChild(submitButton);

    // Set the title and display the modal
    const taskTitle = document.getElementById('taskTitle');
    taskTitle.innerText = `Input for ${taskDescriptions[taskName]}`;
    modal.style.display = "block";

    // Event listener for closing the modal when the 'X' is clicked
    closeButton.onclick = function() {
        modal.style.display = "none";
    };

    // Update form action
    form.onsubmit = (e) => submitTaskForm(e, taskName);
}

function submitTaskForm(event, taskName) {
    event.preventDefault();
    const formData = new FormData(event.target);

    fetch('/run_task', {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error + ": " + err.details);});
        }
        return response.json();
    })
    .then(data => {
        displaySuccess("Task completed successfully!");
        document.getElementById('taskModal').style.display = "none";
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('taskModal').style.display = "none";

        // Optionally, display the error on the page
        displayError(error);
    });
}

function displaySuccess(message) {
    // You can display the success message similarly to how you display errors
    // Perhaps you have a 'successMessage' element in your HTML
    const successElement = document.getElementById('successMessage');
    successElement.innerText = message;
    successElement.style.display = 'block';
}

function displayError(error) {
    // Set the error message
    document.getElementById('errorMessage').innerText = error.message;

    // Show the error modal
    var errorModal = document.getElementById('errorModal');
    errorModal.style.display = 'block';

    // Close event for the 'X' button
    var closeButton = errorModal.querySelector('.close');
    closeButton.onclick = function() {
        errorModal.style.display = 'none';
    };
}

// Close modal logic
window.onclick = function(event) {
    const modal = document.getElementById('taskModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
    var errorModal = document.getElementById('errorModal');
    if (event.target == errorModal) {
        errorModal.style.display = "none";
    }
}
