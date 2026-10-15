const form = document.getElementById("expense-form");
const expenseList = document.getElementById("expense-list");
const totalCount = document.getElementById("total-count");
const totalAmount = document.getElementById("total-amount");
const message = document.getElementById("message");

let expenses = [];

document.getElementById("date").value =
    new Date().toLocaleDateString("en-CA");

function formatAmount(amount) {
    return "Rs " + Number(amount).toLocaleString("en-PK", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function renderExpenses() {
    expenseList.replaceChildren();
    totalCount.textContent = expenses.length;

    const total = expenses.reduce(
        (sum, expense) => sum + Number(expense.amount), 0
    );

    totalAmount.textContent = formatAmount(total);

    if (expenses.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 5;
        cell.textContent = "No expenses added yet.";
        cell.style.textAlign = "center";
        row.appendChild(cell);
        expenseList.appendChild(row);
        return;
    }

    expenses.forEach((expense) => {
        const row = document.createElement("tr");

        [
            expense.title,
            formatAmount(expense.amount),
            expense.category,
            expense.date
        ].forEach((value) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const actionCell = document.createElement("td");
        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-btn";
        deleteButton.type = "button";

        deleteButton.addEventListener("click", async () => {
            try {
                const response = await fetch(
                    `/expenses/${encodeURIComponent(expense.id)}`,
                    { method: "DELETE" }
                );

                if (!response.ok) {
                    throw new Error("Delete failed");
                }

                await loadExpenses();
                message.textContent = "Expense deleted successfully.";
            } catch (error) {
                message.textContent = "Could not delete expense.";
            }
        });

        actionCell.appendChild(deleteButton);
        row.appendChild(actionCell);
        expenseList.appendChild(row);
    });
}

async function loadExpenses() {
    try {
        const response = await fetch("/expenses");

        if (!response.ok) {
            throw new Error("Could not load expenses");
        }

        expenses = await response.json();
        renderExpenses();
    } catch (error) {
        message.textContent =
            "Could not load expenses. Please try again.";
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const amount = Number(document.getElementById("amount").value);
    const category = document.getElementById("category").value;
    const date = document.getElementById("date").value;

    if (!title || !Number.isFinite(amount) ||
        amount <= 0 || !category || !date) {
        message.textContent = "Please enter valid expense details.";
        return;
    }

    try {
        const response = await fetch("/expenses", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, amount, category, date })
        });

        if (!response.ok) {
            throw new Error("Could not save expense");
        }

        await loadExpenses();
        form.reset();

        document.getElementById("date").value =
            new Date().toLocaleDateString("en-CA");

        message.textContent = "Expense added successfully!";
    } catch (error) {
        message.textContent =
            "Could not save expense. Please try again.";
    }
});

loadExpenses();