// main.js - Site-wide JavaScript for Classic Bike Shop

document.addEventListener('DOMContentLoaded', function () {
    
    /**
     * Initializes the mobile menu toggle functionality.
     * Looks for a button with id 'mobile-menu-button' and a menu with id 'mobile-menu'.
     */
    function initMobileMenu() {
        const menuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');

        if (menuButton && mobileMenu) {
            menuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }
    }

    /**
     * Initializes the EMI calculator functionality.
     * Attaches an event listener to the form with id 'emi-form'.
     * Note: Your emi_calculator.html needs the correct IDs for this to work.
     */
    function initEMICalculator() {
        const emiForm = document.getElementById('emi-form');
        const resultDiv = document.getElementById('emi-result');

        if (emiForm && resultDiv) {
            emiForm.addEventListener('submit', function (event) {
                event.preventDefault(); // Prevent the form from submitting the traditional way

                // Clear previous results and hide the result box
                resultDiv.innerHTML = '';
                resultDiv.classList.add('hidden');

                // Get values from the form and convert them to numbers
                const principal = parseFloat(document.getElementById('loanAmount').value);
                const annualRate = parseFloat(document.getElementById('interestRate').value);
                const tenureYears = parseFloat(document.getElementById('loanTenure').value);

                // --- Input Validation ---
                if (isNaN(principal) || principal <= 0 ||
                    isNaN(annualRate) || annualRate < 0 ||
                    isNaN(tenureYears) || tenureYears <= 0) {
                    
                    resultDiv.innerHTML = `<p class="text-red-600 font-semibold">Please enter valid positive numbers for all fields.</p>`;
                    resultDiv.classList.remove('hidden');
                    return;
                }

                // --- Calculation ---
                const monthlyRate = annualRate / (12 * 100); // Monthly interest rate
                const tenureMonths = tenureYears * 12; // Loan tenure in months

                // Handle zero interest rate case
                if (monthlyRate === 0) {
                    const emi = principal / tenureMonths;
                    displayResults(emi, principal, 0);
                    return;
                }
                
                // EMI formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
                const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, tenureMonths)) / (Math.pow(1 + monthlyRate, tenureMonths) - 1);
                
                const totalAmountPayable = emi * tenureMonths;
                const totalInterest = totalAmountPayable - principal;

                // --- Display Results ---
                displayResults(emi, totalAmountPayable, totalInterest);
            });

            function displayResults(emi, totalAmount, totalInterest) {
                 resultDiv.innerHTML = `
                    <h3 class="text-xl font-bold mb-4 text-gray-800">Your Loan Details</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center bg-gray-100 p-3 rounded-lg">
                            <span class="font-semibold text-gray-600">Monthly EMI:</span>
                            <span class="text-2xl font-bold text-blue-600">'₹${emi.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center p-3">
                            <span class="font-semibold text-gray-600">Total Interest Payable:</span>
                            <span class="font-bold text-gray-800">'₹${totalInterest.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center p-3">
                            <span class="font-semibold text-gray-600">Total Amount Payable:</span>
                            <span class="font-bold text-gray-800">'₹${totalAmount.toFixed(2)}</span>
                        </div>
                    </div>
                `;
                resultDiv.classList.remove('hidden');
            }
        }
    }

    /**
     * Initializes client-side form validation for the test drive form.
     * Note: Your test_drive.html needs the correct IDs for this to work.
     */
    function initTestDriveFormValidation() {
        const testDriveForm = document.getElementById('test-drive-form');
        
        if (testDriveForm) {
            testDriveForm.addEventListener('submit', function(event) {
                // Clear previous errors
                document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
                let isValid = true;

                // Helper function to show errors
                const showError = (id, message) => {
                    document.getElementById(id).textContent = message;
                    isValid = false;
                };

                // Validate Name
                if (document.getElementById('name').value.trim() === '') {
                    showError('name-error', 'Full name is required.');
                }

                // Validate Email
                const email = document.getElementById('email');
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (email.value.trim() === '') {
                    showError('email-error', 'Email address is required.');
                } else if (!emailPattern.test(email.value)) {
                    showError('email-error', 'Please enter a valid email address.');
                }

                // Validate Phone
                const phone = document.getElementById('phone');
                const phonePattern = /^\d{10}$/; // Simple 10-digit phone number validation
                if (phone.value.trim() === '') {
                    showError('phone-error', 'Phone number is required.');
                } else if (!phonePattern.test(phone.value)) {
                    showError('phone-error', 'Please enter a valid 10-digit phone number.');
                }
                
                // Validate Bike Selection
                if (document.getElementById('bike').value === '') {
                    showError('bike-error', 'Please select a bike.');
                }

                // Validate Date
                if (document.getElementById('date').value === '') {
                    showError('date-error', 'Please choose a date.');
                }

                if (!isValid) {
                    event.preventDefault(); // Prevent form submission if validation fails
                }
            });
        }
    }
    
    // --- Initialize all modules ---
    initMobileMenu();
    initEMICalculator();
    initTestDriveFormValidation();

    console.log("main.js loaded with detailed functionality.");
});

