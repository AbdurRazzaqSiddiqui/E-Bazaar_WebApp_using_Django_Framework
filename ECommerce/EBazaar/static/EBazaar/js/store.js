document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-mobile-menu]");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll("[data-confirm]").forEach((button) => {
    button.addEventListener("click", (event) => {
      if (!window.confirm(button.dataset.confirm)) event.preventDefault();
    });
  });

  const addressSelect = document.querySelector("select[name='address']");
  const newAddress = document.querySelector("details.new-address");
  if (addressSelect && newAddress) {
    addressSelect.addEventListener("change", () => {
      newAddress.open = !addressSelect.value;
    });
  }
});
