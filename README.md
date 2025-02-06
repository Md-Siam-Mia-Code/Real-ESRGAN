# <p align="center"><div class="gradient-text" style="font-size: 60px;">Real-ESRGAN WebUI Upscaler</div></p>

<p align="center">
  <a href="https://github.com/Md-Siam-Mia/Real-ESRGAN" target="_blank">
    <img src="./assets/ui.png alt="Project Screenshot" width="600px">
  </a>
</p>

<p align="center">
  <a href="https://github.com/Md-Siam-Mia/Real-ESRGAN/releases" target="_blank">
    <img src="https://img.shields.io/github/v/release/Md-Siam-Mia/Real-ESRGAN?style=for-the-badge" alt="GitHub release">
  </a>
  <a href="https://github.com/Md-Siam-Mia/Real-ESRGAN/issues" target="_blank">
    <img src="https://img.shields.io/github/issues/Md-Siam-Mia/Real-ESRGAN?style=for-the-badge" alt="GitHub issues">
  </a>
  <a href="https://github.com/your-github-username/your-repo-name/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/Md-Siam-Mia/Real-ESRGAN?style=for-the-badge" alt="License">
  </a>
</p>

<br/>

## Overview

**Real-ESRGAN WebUI Upscaler** is an intuitive web interface designed to empower you with stunning image upscaling capabilities directly from the convenience of your browser. Built upon the powerful Real-ESRGAN model, this application provides a user-friendly way to transform your low-resolution images into high-definition visuals, enhancing detail and clarity. Whether you're looking to revitalize old photographs, improve low-resolution game textures, or enhance any other image, this WebUI simplifies the process and makes impressive results accessible to everyone.

**Key Features:**

*   **Effortless Image Upscaling:**  Easily enhance your images using the state-of-the-art Real-ESRGAN model.
*   **Web-Based Interface:** Access the application through your web browser – no complex installations or command-line fuss required (beyond initial setup).
*   **Multiple Model Support:** Choose from a variety of Real-ESRGAN models to suit your specific upscaling needs.
*   **TTA Mode:** Enable Tiled Testing (TTA) mode for potentially improved and more detailed results.
*   **GPU Acceleration:** Leverage GPU acceleration for significantly faster processing speeds (NVIDIA GPU recommended).
*   **Vulkan GPU Support:** With Vulkan support it can run on both Intel and AMD GPU.
*   **Progress Monitoring:** Track the upscaling process in real-time with progress bars for individual images and the overall batch.
*   **Batch Processing:** Upscale multiple images simultaneously and download them as a single ZIP file.
*   **Preview Grid:** View previews of both original and processed images side-by-side within the browser.
*   **History Clearing:** Easily clear uploaded and processed images, keeping your workspace tidy.
*   **Download Options:** Download enhanced images individually or as a batch in a ZIP archive for convenience.
*   **Drag and Drop Support:** Enjoy the ease of drag and drop functionality for file uploads.
*   **Responsive Design:**  The interface is designed to be responsive and work seamlessly across both desktop and mobile browsers.

## Installation

Follow these steps to set up the Real-ESRGAN WebUI Upscaler on your local machine.

### Prerequisites

Before proceeding with the installation, ensure you have the following installed:

1.  **Python 3.7+:** Make sure you have Python 3.7 or a newer like 3.12 version installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Real-ESRGAN Executable:** The application relies on the Real-ESRGAN `Real-ESRGAN.exe` executable to perform the upscaling. You can download this from the official Real-ESRGAN GitHub repository: [https://github.com/xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN). Follow the instructions there to download the Windows demo with pre-trained models. After downloading `Real-ESRGAN.exe`, ensure it is placed within a folder named `realesrgan` in your project's root directory.

3.  **NVIDIA GPU (Recommended):** While the application can run on a CPU, an NVIDIA graphics card with CUDA support is highly recommended for significantly faster processing speeds. CPU processing will be considerably slower.

4.  **`git` (Optional):** Git is optional but recommended for cloning the GitHub repository. If you don't have Git, you can download the repository as a ZIP file directly from GitHub. Git can be installed from [https://git-scm.com/downloads](https://git-scm.com/downloads).

5. **Conda Environment (optional):** Use a virtual conda environment instead of running it globally on you system.

### Installation Steps

1.  **Clone the Repository (or Download ZIP):**

    Using Git, clone the repository:

    ```bash
    git clone [https://github.com/Md-Siam-Mia/Real-ESRGAN.git](https://github.com/Md-Siam-Mia/Real-ESRGAN.git)
    cd your-repo-name
    ```

    Alternatively, you can download the repository as a ZIP file from GitHub and extract it to your desired directory.

2.  **Create a Virtual Conda Environment (Recommended):**

    Creating a virtual environment helps isolate the project's dependencies from your system-wide Python installation.

    ```bash
    conda create -n Real-ESRGAN python=3.12 -y
    ```

    Activate the virtual environment:

    *   **Windows:** **Linux/macOS:**

        ```bash
        conda activate Real-ESRGAN
        ```

3.  **Install Python Dependencies:**

    Use the `requirements.txt` file to install the necessary Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Place Real-ESRGAN Executable:**

    Ensure that the `Real-ESRGAN.exe` executable is placed in a folder named `realesrgan` within the root of your project directory. Your project structure should look like this:

    ```
    Real-ESRGAN/
    ├── app.py
    ├── templates/
    ├── realesrgan/
    │   └── Real-ESRGAN.exe
    ├── requirements.txt
    ├── README.md
    └── ...
    ```

5.  **Run the Application:**

    Start the Flask application by using the following command in your terminal:

    ```bash
    python app.py
    ```

    The application should now be accessible at `http://127.0.0.1:3010/` in your web browser.

## Usage

1.  Navigate to `http://127.0.0.1:3010/` in your web browser.
2.  Drag and drop images into the "Drag and drop images here" zone, or click the zone to use the file input dialog.
3.  Select the **TTA Mode** checkbox if desired for potentially enhanced results.
4.  Choose your preferred **GPU** from the dropdown menu (if applicable). "Default GPU" will run on the CPU.
5.  Select a **Model** from the dropdown menu. The options include various Real-ESRGAN models for different upscaling characteristics.
6.  Click the **Upscale Images** button to begin the upscaling process.
7.  Monitor the progress of each image and the total batch using the progress bars.
8.  Once processing is complete, the enhanced images will appear in the "Processed Images" section.
9.  Download images individually by clicking the **Download** button under each processed image, or download all processed images as a ZIP file using the **Download All** button.
10. Clear input and output images using the **Clear History** button.
11. Refresh the web page using the **Reload UI** button.

## Customization

*   **Real-ESRGAN Models:** The application supports various Real-ESRGAN models. You can modify the `model` select options in the `index.html` file to add more models or remove existing ones. Ensure that the selected models are compatible with the `Real-ESRGAN.exe` executable you are using.

*   **CSS Theme:** To customize the visual appearance of the application, you can edit the CSS on the `index.html`. The main CSS variables are defined in the `:root` selector, allowing you to easily change the project's color scheme.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, and pull requests.

When contributing, please ensure that:

*   Your code is clean and well-commented.
*   You have added relevant tests for any new features or bug fixes.
*   Your changes do not break existing functionality.

## License

The main executables are provided by a open source project named Real-ESRGAN by [https://github.com/xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN).

## Disclaimer

*   This application is graphics-intensive and benefits significantly from a compatible NVIDIA GPU for acceleration. You can also use a Intel or AMD gpu with vulkan support. CPU processing is possible but will be considerably slower and this project may not run on some cpus.

*   The provided `Real-ESRGAN.exe` executable is a third-party tool and is distributed under its own license. Please ensure you review their license terms.

## Author

[Md. Siam Mia] - [[Your GitHub Profile Link](https://github.com/Md-Siam-Mia/Real-ESRGAN.git)] - [mdsiammia.main@gmail.com]

---

More features will added via updates later. Thank you for using the Real-ESRGAN WebUI Upscaler!