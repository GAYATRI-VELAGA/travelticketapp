const API = "http://127.0.0.1:8000";

const $ = (id) => document.getElementById(id);

function showMessage(text, error = false) {
    const box = $("message");
    box.textContent = text;
    box.className = "message" + (error ? " error" : "");
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function apiRequest(url, options = {}) {
    const response = await fetch(url, options);
    const text = await response.text();

    let data;
    try {
        data = text ? JSON.parse(text) : {};
    } catch {
        data = { detail: text };
    }

    if (!response.ok) {
        throw new Error(data.detail || data.message || `Request failed (${response.status})`);
    }

    return data;
}

async function checkApi() {
    try {
        const data = await apiRequest(`${API}/`);
        $("apiStatus").textContent = "● API Connected";
        $("apiStatus").style.color = "#17663a";
    } catch (error) {
        $("apiStatus").textContent = "● API Offline";
        $("apiStatus").style.color = "#a52727";
    }
}

$("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const params = new URLSearchParams({
        name: $("regName").value,
        email: $("regEmail").value,
        phone: $("regPhone").value,
        password: $("regPassword").value
    });

    try {
        const data = await apiRequest(`${API}/register?${params}`, { method: "POST" });
        showMessage(`${data.message}. User ID: ${data.user_id}`);
        e.target.reset();
    } catch (error) {
        showMessage(error.message, true);
    }
});

$("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const params = new URLSearchParams({
        email: $("loginEmail").value,
        password: $("loginPassword").value
    });

    try {
        const data = await apiRequest(`${API}/login?${params}`, { method: "POST" });

        if (data.user_id) {
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_name", data.name || "");
            $("loggedUser").textContent = `Logged in: ${data.name} (User ID: ${data.user_id})`;
            $("ownerId").value = data.user_id;
        }

        showMessage(data.message);
    } catch (error) {
        showMessage(error.message, true);
    }
});

$("ticketForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const params = new URLSearchParams({
        owner_id: $("ownerId").value,
        passenger_name: $("passengerName").value,
        from_location: $("fromLocation").value,
        to_location: $("toLocation").value,
        travel_date: $("travelDate").value,
        travel_time: $("travelTime").value,
        seat_number: $("seatNumber").value,
        original_price: $("originalPrice").value
    });

    try {
        const data = await apiRequest(`${API}/tickets?${params}`, { method: "POST" });
        showMessage(`${data.message}. Ticket ID: ${data.ticket_id}`);
        e.target.reset();

        const savedUser = localStorage.getItem("user_id");
        if (savedUser) $("ownerId").value = savedUser;

        await loadTickets();
    } catch (error) {
        showMessage(error.message, true);
    }
});

$("sellForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const ticketId = $("sellTicketId").value;
    const price = $("sellingPrice").value;

    try {
        const data = await apiRequest(
            `${API}/tickets/${ticketId}/sell?selling_price=${encodeURIComponent(price)}`,
            { method: "PUT" }
        );

        showMessage(`${data.message}. Ticket ${data.ticket_id} is now ${data.status}.`);
        e.target.reset();
        await loadTickets();
    } catch (error) {
        showMessage(error.message, true);
    }
});

async function buyTicket(ticketId) {
    let buyerId = localStorage.getItem("user_id");

    if (!buyerId) {
        buyerId = prompt("Enter buyer user ID:");
    }

    if (!buyerId) return;

    try {
        const data = await apiRequest(
            `${API}/tickets/${ticketId}/buy?buyer_id=${encodeURIComponent(buyerId)}`,
            { method: "POST" }
        );

        showMessage(`${data.message}. Ticket ${data.ticket_id} is now ${data.status}.`);
        await loadTickets();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function loadTickets() {
    const box = $("tickets");
    box.innerHTML = `<div class="empty">Loading tickets...</div>`;

    try {
        const tickets = await apiRequest(`${API}/tickets/available`);
        $("ticketCount").textContent = tickets.length;

        if (!tickets.length) {
            box.innerHTML = `<div class="empty">No tickets are currently available.</div>`;
            return;
        }

        box.innerHTML = tickets.map(ticket => `
            <article class="ticket">
                <div class="route">${escapeHtml(ticket.from_location)} → ${escapeHtml(ticket.to_location)}</div>
                <span class="badge">${escapeHtml(ticket.status)}</span>
                <div class="price">₹${Number(ticket.selling_price ?? ticket.original_price).toFixed(2)}</div>

                <div class="ticket-row"><span>Ticket ID</span><strong>${ticket.id}</strong></div>
                <div class="ticket-row"><span>Passenger</span><span>${escapeHtml(ticket.passenger_name)}</span></div>
                <div class="ticket-row"><span>Date</span><span>${ticket.travel_date}</span></div>
                <div class="ticket-row"><span>Time</span><span>${ticket.travel_time}</span></div>
                <div class="ticket-row"><span>Seat</span><span>${escapeHtml(ticket.seat_number)}</span></div>

                <button class="buy-btn" onclick="buyTicket(${ticket.id})">Buy Ticket</button>
            </article>
        `).join("");
    } catch (error) {
        $("ticketCount").textContent = "0";
        box.innerHTML = `<div class="empty">Could not load tickets: ${escapeHtml(error.message)}</div>`;
    }
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

$("refreshBtn").addEventListener("click", loadTickets);

window.addEventListener("DOMContentLoaded", async () => {
    const savedUser = localStorage.getItem("user_id");
    const savedName = localStorage.getItem("user_name");

    if (savedUser) {
        $("loggedUser").textContent = `Logged in: ${savedName || "User"} (User ID: ${savedUser})`;
        $("ownerId").value = savedUser;
    }

    await checkApi();
    await loadTickets();
});
