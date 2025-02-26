document.addEventListener('DOMContentLoaded', function() {
    // Add Project
    document.getElementById('add-project').addEventListener('click', function() {
        const projectsDiv = document.getElementById('projects');
        const newProject = document.createElement('div');
        newProject.classList.add('project');
        newProject.innerHTML = `
            <label for="project">Project:</label>
            <input type="text" name="project[]"><br>
            <label for="project_description">Project Description:</label>
            <textarea name="project_description[]"></textarea><br>
            <label for="project_link">Project Link:</label>
            <input type="text" name="project_link[]"><br>
            <button type="button" class="remove-project">Remove Project</button><br><br>
        `;
        projectsDiv.appendChild(newProject);
    });

    // Remove Project
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-project')) {
            event.target.parentElement.remove();
        }
    });

    // Add Language
    document.getElementById('add-language').addEventListener('click', function() {
        const languagesDiv = document.getElementById('languages');
        const newLanguage = document.createElement('div');
        newLanguage.classList.add('language');
        newLanguage.innerHTML = `
            <label for="language">Language:</label>
            <input type="text" name="language[]"><br>
            <button type="button" class="remove-language">Remove Language</button><br><br>
        `;
        languagesDiv.appendChild(newLanguage);
    });

    // Remove Language
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-language')) {
            event.target.parentElement.remove();
        }
    });
});