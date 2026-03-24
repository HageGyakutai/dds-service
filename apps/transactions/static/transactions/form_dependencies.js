(function () {
  const form = document.getElementById("cashflow-record-form");
  if (!form) return;

  const operationTypeSelect = document.getElementById("id_operation_type");
  const categorySelect = document.getElementById("id_category");
  const subcategorySelect = document.getElementById("id_subcategory");

  if (!operationTypeSelect || !categorySelect || !subcategorySelect) return;

  const categoriesUrl = form.dataset.categoriesUrl;
  const subcategoriesUrl = form.dataset.subcategoriesUrl;

  const initialCategory = form.dataset.initialCategory || "";
  const initialSubcategory = form.dataset.initialSubcategory || "";

  function resetSelect(selectElement, disabled = true) {
    selectElement.innerHTML = "";
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "---------";
    selectElement.appendChild(placeholder);
    selectElement.disabled = disabled;
  }

  function fillSelect(selectElement, items, selectedValue = "") {
    resetSelect(selectElement, items.length === 0);

    items.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = item.name;
      selectElement.appendChild(option);
    });

    if (selectedValue) {
      selectElement.value = selectedValue;
    }
  }

  async function fetchResults(url, params) {
    const query = new URLSearchParams(params);
    const response = await fetch(`${url}?${query.toString()}`, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });

    if (!response.ok) {
      return [];
    }

    const payload = await response.json();
    return payload.results || [];
  }

  async function loadCategories(operationTypeId, selectedCategory = "") {
    if (!operationTypeId) {
      resetSelect(categorySelect, true);
      resetSelect(subcategorySelect, true);
      return;
    }

    const categories = await fetchResults(categoriesUrl, {
      operation_type_id: operationTypeId,
    });

    fillSelect(categorySelect, categories, selectedCategory);
    resetSelect(subcategorySelect, true);
  }

 async function loadSubcategories(categoryId, selectedSubcategory = "") {
    if (!categoryId) {
      resetSelect(subcategorySelect, true);
      return;
    }

    const subcategories = await fetchResults(subcategoriesUrl, {
      category_id: categoryId,
    });

    fillSelect(subcategorySelect, subcategories, selectedSubcategory);
  }

  operationTypeSelect.addEventListener("change", async () => {
    await loadCategories(operationTypeSelect.value, "");
  });

  categorySelect.addEventListener("change", async () => {
    await loadSubcategories(categorySelect.value, "");
  });

 (async function init() {
    const selectedOperationType = operationTypeSelect.value;
    const selectedCategory = categorySelect.value || initialCategory;
    const selectedSubcategory = subcategorySelect.value || initialSubcategory;

    if (!selectedOperationType) {
      resetSelect(categorySelect, true);
      resetSelect(subcategorySelect, true);
      return;
    }

    await loadCategories(selectedOperationType, selectedCategory);

    if (categorySelect.value) {
      await loadSubcategories(categorySelect.value, selectedSubcategory);
    }
  })();
})();


