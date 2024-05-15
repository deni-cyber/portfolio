document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('container');
    const box = document.getElementById('box');
    let position = 0;
    let velocity = 0;
    const gravity = 0.3;
    const bounceFactor = 0.6;

    function dropAndBounce() {
        // Apply gravity to velocity
        velocity += gravity;
        // Update position based on velocity
        position += velocity;
        // Get the maximum bottom position within the container
        const maxPosition = container.clientHeight - box.clientHeight;
        // Check if the box has reached the bottom of the container
        if (position >= maxPosition) {
            // Reverse velocity with bounce factor
            velocity *= -bounceFactor;
            // Keep box within the container boundaries
            position = maxPosition;
        }
        // Update box position
        box.style.top = position + 'px';
    }

    // Set animation loop using setInterval
    const animationInterval = setInterval(dropAndBounce, 16); // 60 FPS (1000 ms / 60)
    
    // Stop animation after 3 seconds (adjust duration as needed)
    setTimeout(() => {
        clearInterval(animationInterval);
    }, 3000); // Stop after 3 seconds
});