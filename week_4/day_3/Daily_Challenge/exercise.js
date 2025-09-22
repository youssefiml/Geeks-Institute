class Video {
  constructor(title, uploader, time) {
    this.title = title;
    this.uploader = uploader;
    this.time = time;
  }

  watch() {
    console.log(`${this.uploader} watched all ${this.time} seconds of "${this.title}"!`);
  }
}

const video1 = new Video("Learn JavaScript Basics", "Youssef", 300);
video1.watch();

const video2 = new Video("Mastering CSS Grid", "Sami", 600);
video2.watch();

const videoData = [
  { title: "React Tutorial", uploader: "Nicky", time: 1200 },
  { title: "Node.js Crash Course", uploader: "Lina", time: 1500 },
  { title: "CSS Flexbox Deep Dive", uploader: "Jack", time: 800 },
  { title: "Python for Beginners", uploader: "Soufia", time: 2000 },
  { title: "Git & GitHub Basics", uploader: "Lana", time: 900 },
];

const videoInstances = videoData.map(data => new Video(data.title, data.uploader, data.time));
videoInstances.forEach(video => video.watch());
