// 手机菜单
const menuBtn = document.querySelector(".menu-btn");
const nav = document.getElementById("nav");
menuBtn.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", String(open));
});
nav.addEventListener("click", (e) => {
  if (e.target.tagName === "A") {
    nav.classList.remove("open");
    menuBtn.setAttribute("aria-expanded", "false");
  }
});

// 滚动渐显
const reveals = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add("in");
        io.unobserve(en.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px" });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add("in"));
}

// 画廊大图
const lb = document.querySelector(".lightbox");
const lbImg = lb.querySelector("img");
document.querySelectorAll(".g-item").forEach((btn) => {
  btn.addEventListener("click", () => {
    lbImg.src = btn.dataset.full;
    lb.showModal();
  });
});
lb.addEventListener("click", (e) => {
  if (e.target !== lbImg) lb.close();
});

// 复制微信号
document.querySelectorAll(".copy-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const label = btn.textContent;
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      btn.textContent = btn.dataset.done;
    } catch {
      const r = document.createRange();
      r.selectNodeContents(document.getElementById("wechat-id"));
      getSelection().removeAllRanges();
      getSelection().addRange(r);
    }
    setTimeout(() => { btn.textContent = label; }, 1800);
  });
});
