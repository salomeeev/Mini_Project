document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    if (!searchForm) return; // Only run on pages with the search/filters form

    const searchInput = document.getElementById('searchInput');
    const deptSelect = document.getElementById('deptFilter');
    const desigSelect = document.getElementById('desigFilter');
    const statusSelect = document.getElementById('statusFilter');
    const genderSelect = document.getElementById('genderFilter');
    const sortSelect = document.getElementById('sortFilter');
    const tableContainer = document.getElementById('employeeTableContainer');
    
    let debounceTimer;

    function buildQueryString(page = 1) {
        const params = new URLSearchParams();
        if (searchInput && searchInput.value) params.append('search', searchInput.value);
        if (deptSelect && deptSelect.value) params.append('department', deptSelect.value);
        if (desigSelect && desigSelect.value) params.append('designation', desigSelect.value);
        if (statusSelect && statusSelect.value) params.append('status', statusSelect.value);
        if (genderSelect && genderSelect.value) params.append('gender', genderSelect.value);
        if (sortSelect && sortSelect.value) params.append('sort', sortSelect.value);
        params.append('page', page);
        params.append('ajax', '1');
        return params.toString();
    }

    function updateResults(page = 1) {
        showLoading();
        const queryString = buildQueryString(page);
        const url = `${window.location.pathname}?${queryString}`;

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (tableContainer) {
                tableContainer.innerHTML = data.html;
                // Re-bind click events to new pagination/sort elements inside the container
                bindInteractiveElements();
            }
            // Update browser URL query string without reloading page
            const cleanQueryString = queryString.replace('&ajax=1', '');
            const newUrl = `${window.location.pathname}?${cleanQueryString}`;
            window.history.pushState({ path: newUrl }, '', newUrl);
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        })
        .finally(() => {
            hideLoading();
        });
    }

    function bindInteractiveElements() {
        // Intercept clicks on pagination links
        const paginationLinks = tableContainer.querySelectorAll('.pagination-custom .page-link');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const pageUrl = new URL(this.href);
                const pageNum = pageUrl.searchParams.get('page') || 1;
                updateResults(pageNum);
            });
        });

        // Intercept sorting header links if present
        const sortHeaders = tableContainer.querySelectorAll('.sort-link');
        sortHeaders.forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const sortVal = this.dataset.sort;
                if (sortSelect) {
                    sortSelect.value = sortVal;
                    // Trigger select change logic
                    updateResults(1);
                }
            });
        });
    }

    // Event Listeners for Filters
    const filters = [deptSelect, desigSelect, statusSelect, genderSelect, sortSelect];
    filters.forEach(filter => {
        if (filter) {
            filter.addEventListener('change', function () {
                updateResults(1);
            });
        }
    });

    // Debounced search text input
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                updateResults(1);
            }, 350); // 350ms debounce
        });

        // Prevent enter key from submitting form (which causes reload)
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
            }
        });
    }

    // Initial binding
    bindInteractiveElements();
});
