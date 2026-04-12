from flask import Blueprint, render_template, session, redirect, Response
import pandas as pd
import matplotlib

# ✅ IMPORTANT: prevent GUI backend issues (server-safe)
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io

from db import get_user_by_username, get_connection

# ✅ blueprint name MUST match url_for('dashboard.*')
dashboard_bp = Blueprint('dashboard', __name__)


# -------------------------------
# DASHBOARD VIEW
# -------------------------------
@dashboard_bp.route('/dashboard')
def dashboard_view():
    if 'username' not in session:
        return redirect('/login')

    user = get_user_by_username(session['username'])
    if not user:
        session.clear()
        return redirect('/login')

    return render_template(
        'login_interface.html',
        username=user["username"],
        balance=user["balance"]
    )

# -------------------------------
# TRANSACTION SUMMARY
# -------------------------------
@dashboard_bp.route('/plot/transactions.png')
def plot_transactions():
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT type, amount FROM transactions", conn)
    finally:
        conn.close()

    fig, ax = plt.subplots(figsize=(8, 5))

    if df.empty or not {'type', 'amount'}.issubset(df.columns):
        ax.text(0.5, 0.5, 'No transaction data',
                ha='center', va='center')
        ax.set_axis_off()
    else:
        summary = df.groupby('type')['amount'].sum()
        summary.plot(kind='bar', ax=ax)

        ax.set_title('Transaction Summary')
        ax.set_xlabel('Type')
        ax.set_ylabel('Amount')

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(
        buf.getvalue(),
        mimetype='image/png',
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )


# -------------------------------
# USER HISTORY CHART
# -------------------------------
@dashboard_bp.route('/plot/history.png')
def plot_history():
    if 'username' not in session:
        return Response("Not logged in", status=401)

    user = get_user_by_username(session['username'])
    if not user:
        session.clear()
        return Response("User not found", status=401)

    conn = get_connection()
    try:
        df = pd.read_sql_query(
            "SELECT timestamp, amount FROM transactions WHERE user_id = ?",
            conn,
            params=(user['id'],),
            parse_dates=['timestamp']
        )
    finally:
        conn.close()

    fig, ax = plt.subplots(figsize=(10, 5))

    if df.empty or not {'timestamp', 'amount'}.issubset(df.columns):
        ax.text(0.5, 0.5, 'No history available',
                ha='center', va='center')
        ax.set_axis_off()
    else:
        # ✅ clean data
        df = df.dropna(subset=['timestamp'])
        df = df.sort_values('timestamp')
        df.set_index('timestamp', inplace=True)

        # ✅ DAILY aggregation (THIS IS WHAT YOU WANT)
        ts = df.resample('D')['amount'].sum()

        if ts.empty:
            ax.text(0.5, 0.5, 'No transaction data',
                    ha='center', va='center')
            ax.set_axis_off()
        else:
            # ✅ line graph
            ts.plot(ax=ax, marker='o')

            ax.set_title("Daily Transaction History")
            ax.set_xlabel('Date')
            ax.set_ylabel('Amount')

            # ✅ better readability
            ax.tick_params(axis='x', rotation=45)

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(
        buf.getvalue(),
        mimetype='image/png',
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
        }
    )

# -------------------------------
# USER HOURLY HISTORY CHART
# -------------------------------
@dashboard_bp.route('/plot/hourly.png')
def plot_hourly():
    if 'username' not in session:
        return Response("Not logged in", status=401)

    user = get_user_by_username(session['username'])
    if not user:
        session.clear()
        return Response("User not found", status=401)

    conn = get_connection()
    try:
        df = pd.read_sql_query(
            "SELECT timestamp, amount FROM transactions WHERE user_id = ?",
            conn,
            params=(user['id'],)
        )
    finally:
        conn.close()

    fig, ax = plt.subplots(figsize=(10, 5))

    if df.empty:
        ax.text(0.5, 0.5, 'No transactions found',
                ha='center', va='center')
        ax.set_axis_off()
    else:
        # 🔥 FORCE datetime conversion (no assumptions)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])

        if df.empty:
            ax.text(0.5, 0.5, 'Invalid timestamps',
                    ha='center', va='center')
            ax.set_axis_off()
        else:
            df = df.sort_values('timestamp')

            print("DATA:", df.tail())  # 🔍 DEBUG

            # ✅ DIRECT plotting (NO resample, NO filter)
            ax.plot(df['timestamp'], df['amount'], marker='o')

            ax.set_title("Transaction Timeline (Raw Time)")
            ax.set_xlabel("Time")
            ax.set_ylabel("Amount")
            ax.tick_params(axis='x', rotation=45)

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(
        buf.getvalue(),
        mimetype='image/png',
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
        }
    )