const API_URL = "http://127.0.0.1:8000";
const PAGE_LIMIT = 10;

const statusElement = document.getElementById("status");
const carsListElement = document.getElementById("cars-list");
const filtersForm = document.getElementById("filters-form");
const brandModelFilter = document.getElementById("filter-brand-model");
const fuelFilter = document.getElementById("filter-fuel");
const minYearFilter = document.getElementById("filter-min-year");
const previousPageButton = document.getElementById("page-prev");
const nextPageButton = document.getElementById("page-next");
const addCarButton = document.getElementById("add-car-button");
const carModal = document.getElementById("car-modal");
const carForm = document.getElementById("car-form");
const closeCarModalButton = document.getElementById("close-car-modal");
const cancelCarButton = document.getElementById("cancel-car");
const submitCarButton = document.getElementById("submit-car");
const carModalTitle = document.getElementById("car-modal-title");
const errorBanner = document.getElementById("error-banner");

let currentPage = 1;
let displayedCars = [];
let editingCarId = null;
let appliedFilters = {
  brand_model: "",
  fuel: "",
  min_year: "",
};

function hideError() {
  errorBanner.hidden = true;
  errorBanner.textContent = "";
}

function showApiError(status) {
  const messages = {
    404: "Автомобіль не знайдено. Можливо, його вже видалено",
    409: "Автомобіль із таким VIN уже існує",
    422: "Перевірте правильність заповнення форми",
  };

  errorBanner.textContent =
    messages[status] ?? "Сталася помилка під час виконання запиту. Спробуйте ще раз";
  errorBanner.hidden = false;
}

function showNetworkError() {
  errorBanner.textContent =
    "Не вдалося з'єднатися із сервером. Перевірте, чи запущений бекенд";
  errorBanner.hidden = false;
}

const carFields = [
  ["brand_model", "Марка та модель"],
  ["manufacturer", "Виробник"],
  ["vin", "VIN"],
  ["body_type", "Тип кузова"],
  ["engine_volume", "Об'єм двигуна"],
  ["fuel", "Тип пального"],
  ["price", "Ціна"],
  ["rating", "Рейтинг"],
  ["description", "Опис"],
  ["year", "Рік"],
  ["options", "Опції"],
];

function formatValue(value) {
  if (value === null || value === undefined || value === "") {
    return "—";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

function renderCars(cars) {
  displayedCars = cars;
  carsListElement.replaceChildren();

  if (cars.length === 0) {
    carsListElement.hidden = true;
    statusElement.textContent = "Автомобілів поки немає";
    statusElement.hidden = false;
    return;
  }

  for (const car of cars) {
    const card = document.createElement("article");
    card.className = "car-card";

    const title = document.createElement("h2");
    title.textContent = formatValue(car.brand_model);
    card.appendChild(title);

    const details = document.createElement("dl");
    details.className = "car-details";

    for (const [field, label] of carFields) {
      const term = document.createElement("dt");
      term.textContent = label;

      const description = document.createElement("dd");
      description.textContent = formatValue(car[field]);

      details.append(term, description);
    }

    card.appendChild(details);

    const actions = document.createElement("div");
    actions.className = "car-actions";

    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.textContent = "Редагувати";
    editButton.addEventListener("click", () => openCarModal(car));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "delete-car-button";
    deleteButton.textContent = "Видалити";
    deleteButton.addEventListener("click", () => deleteCar(car.id));

    actions.append(editButton, deleteButton);
    card.appendChild(actions);
    carsListElement.appendChild(card);
  }

  statusElement.hidden = true;
  carsListElement.hidden = false;
}

async function loadCars() {
  statusElement.textContent = "Завантаження...";
  statusElement.hidden = false;
  carsListElement.hidden = true;

  try {
    const params = new URLSearchParams({
      page: String(currentPage),
      limit: String(PAGE_LIMIT),
    });
    for (const [name, value] of Object.entries(appliedFilters)) {
      if (value !== "") {
        params.set(name, value);
      }
    }

    let response;
    try {
      response = await fetch(`${API_URL}/cars/?${params.toString()}`);
    } catch (error) {
      console.error("Не вдалося завантажити список автомобілів:", error);
      showNetworkError();
      statusElement.textContent = "Не вдалося завантажити список автомобілів.";
      statusElement.hidden = false;
      carsListElement.hidden = true;
      return;
    }

    if (!response.ok) {
      console.error("Не вдалося завантажити список автомобілів:", response.status);
      showApiError(response.status);
      statusElement.textContent = "Не вдалося завантажити список автомобілів.";
      statusElement.hidden = false;
      carsListElement.hidden = true;
      return;
    }

    try {
      const cars = await response.json();
      if (!Array.isArray(cars)) {
        throw new TypeError("Очікувався список автомобілів у форматі масиву");
      }

      renderCars(cars);
      hideError();
    } catch (error) {
      console.error("Не вдалося обробити список автомобілів:", error);
      showApiError(500);
      statusElement.textContent = "Не вдалося завантажити список автомобілів.";
      statusElement.hidden = false;
      carsListElement.hidden = true;
    }
  } catch (error) {
    console.error("Не вдалося завантажити список автомобілів:", error);
    showApiError(500);
    statusElement.textContent = "Не вдалося завантажити список автомобілів.";
    statusElement.hidden = false;
    carsListElement.hidden = true;
  }
}

function clearCarFormErrors() {
  carForm.querySelectorAll(".field-error").forEach((element) => {
    element.textContent = "";
  });
}

function validateCar(data) {
  const errors = {};
  const validateText = (field, label, value, minLength, maxLength) => {
    if (value.length < minLength || value.length > maxLength) {
      errors[field] = `${label}: від ${minLength} до ${maxLength} символів`;
    }
  };

  validateText("brand_model", "Марка та модель", data.brand_model, 2, 100);
  validateText("manufacturer", "Виробник", data.manufacturer, 2, 100);

  if (data.vin.length !== 17) {
    errors.vin = "VIN має містити рівно 17 символів";
  }

  validateText("body_type", "Тип кузова", data.body_type, 5, 50);

  if (data.engine_volume !== null && (!Number.isFinite(data.engine_volume) || data.engine_volume <= 0)) {
    errors.engine_volume = "Вкажіть число більше 0";
  }

  if (data.fuel !== null) {
    validateText("fuel", "Тип пального", data.fuel, 5, 50);
  }

  if (!Number.isFinite(data.price) || data.price <= 0) {
    errors.price = "Ціна має бути числом більше 0";
  }

  if (data.rating !== null && (!Number.isFinite(data.rating) || data.rating <= 0)) {
    errors.rating = "Рейтинг має бути числом більше 0";
  }

  if (data.description !== null && data.description.length > 500) {
    errors.description = "Опис не може перевищувати 500 символів";
  }

  if (!Number.isInteger(data.year)) {
    errors.year = "Вкажіть цілий рік випуску";
  }

  return errors;
}

function readCarFormData() {
  const value = (name) => carForm.elements[name].value.trim();
  const optionalNumber = (name) => (value(name) === "" ? null : Number(value(name)));

  return {
    brand_model: value("brand_model"),
    manufacturer: value("manufacturer"),
    vin: value("vin"),
    body_type: value("body_type"),
    engine_volume: optionalNumber("engine_volume"),
    fuel: value("fuel") || null,
    price: value("price") === "" ? NaN : Number(value("price")),
    rating: optionalNumber("rating"),
    is_available: value("is_available") === "true",
    description: value("description") || null,
    year: value("year") === "" ? NaN : Number(value("year")),
    options: value("options")
      .split(",")
      .map((option) => option.trim())
      .filter((option) => option !== ""),
  };
}

function showCarFormErrors(errors) {
  for (const [field, message] of Object.entries(errors)) {
    const errorElement = carForm.querySelector(`[data-error-for="${field}"]`);
    if (errorElement) {
      errorElement.textContent = message;
    }
  }
}

function setFormValue(name, value) {
  const field = carForm.elements[name];
  const stringValue = value === null || value === undefined ? "" : String(value);

  if (field instanceof HTMLSelectElement && stringValue !== "") {
    const hasOption = Array.from(field.options).some((option) => option.value === stringValue);
    if (!hasOption) {
      field.add(new Option(stringValue, stringValue));
    }
  }

  field.value = stringValue;
}

function openCarModal(car = null) {
  carForm.reset();
  clearCarFormErrors();
  editingCarId = car ? car.id : null;
  carModalTitle.textContent = car ? "Редагувати автомобіль" : "Додати автомобіль";
  submitCarButton.textContent = car ? "Зберегти зміни" : "Створити автомобіль";
  carForm.elements.vin.readOnly = Boolean(car);

  if (car) {
    for (const field of [
      "brand_model",
      "manufacturer",
      "vin",
      "body_type",
      "engine_volume",
      "fuel",
      "price",
      "rating",
      "is_available",
      "description",
      "year",
    ]) {
      const value = field === "is_available" ? String(car[field]) : car[field];
      setFormValue(field, value);
    }
    setFormValue("options", Array.isArray(car.options) ? car.options.join(", ") : "");
  }

  carModal.hidden = false;
  carForm.elements.brand_model.focus();
}

function closeCarModal() {
  carModal.hidden = true;
  editingCarId = null;
  clearCarFormErrors();
  addCarButton.focus();
}

async function createCar(data) {
  const payload = {
    ...data,
    created_at: new Date().toISOString(),
  };

  submitCarButton.disabled = true;

  try {
    const response = await fetch(`${API_URL}/cars/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (response.status !== 201) {
      console.error("Не вдалося створити автомобіль:", response.status);
      console.error("Не вдалося створити автомобіль:", response.status);
      showApiError(response.status);
      return;
    }

    closeCarModal();
    await loadCars();
  } catch (error) {
    console.error("Не вдалося створити автомобіль:", error);
    console.error("Не вдалося створити автомобіль:", error);
    showNetworkError();
  } finally {
    submitCarButton.disabled = false;
  }
}

async function updateCar(carId, data) {
  const {
    brand_model,
    manufacturer,
    body_type,
    engine_volume,
    fuel,
    price,
    rating,
    is_available,
    description,
    year,
    options,
  } = data;
  const payload = {
    brand_model,
    manufacturer,
    body_type,
    engine_volume,
    fuel,
    price,
    rating,
    is_available,
    description,
    year,
    options,
  };

  submitCarButton.disabled = true;

  try {
    const response = await fetch(`${API_URL}/cars/${carId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      console.error("Не вдалося оновити автомобіль:", response.status);
      showApiError(response.status);
      return;
    }

    hideError();
    closeCarModal();
    await loadCars();
  } catch (error) {
    console.error("Не вдалося оновити автомобіль:", error);
    showNetworkError();
  } finally {
    submitCarButton.disabled = false;
  }
}

async function deleteCar(carId) {
  if (!confirm("Видалити цей автомобіль?")) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/cars/${carId}`, { method: "DELETE" });
    if (!response.ok) {
      console.error("Не вдалося видалити автомобіль:", response.status);
      showApiError(response.status);
      return;
    }

    hideError();
    if (displayedCars.length === 1 && currentPage > 1) {
      currentPage -= 1;
    }
    previousPageButton.disabled = currentPage === 1;
    await loadCars();
  } catch (error) {
    console.error("Не вдалося видалити автомобіль:", error);
    showNetworkError();
  }
}

addCarButton.addEventListener("click", () => openCarModal());
closeCarModalButton.addEventListener("click", closeCarModal);
cancelCarButton.addEventListener("click", closeCarModal);

carModal.addEventListener("click", (event) => {
  if (event.target === carModal) {
    closeCarModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !carModal.hidden) {
    closeCarModal();
  }
});

carForm.addEventListener("submit", (event) => {
  event.preventDefault();
  clearCarFormErrors();

  const data = readCarFormData();
  const errors = validateCar(data);
  if (Object.keys(errors).length > 0) {
    showCarFormErrors(errors);
    return;
  }

  if (editingCarId === null) {
    createCar(data);
  } else {
    updateCar(editingCarId, data);
  }
});

filtersForm.addEventListener("submit", (event) => {
  event.preventDefault();
  appliedFilters = {
    brand_model: brandModelFilter.value.trim(),
    fuel: fuelFilter.value.trim(),
    min_year: minYearFilter.value.trim(),
  };
  currentPage = 1;
  previousPageButton.disabled = true;
  loadCars();
});

previousPageButton.addEventListener("click", () => {
  if (currentPage === 1) {
    return;
  }

  currentPage -= 1;
  previousPageButton.disabled = currentPage === 1;
  loadCars();
});

nextPageButton.addEventListener("click", () => {
  currentPage += 1;
  previousPageButton.disabled = false;
  loadCars();
});

loadCars();
