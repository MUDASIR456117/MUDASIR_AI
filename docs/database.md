# MongoDB Database Architecture — AI Financial Advisor

Database Name: `ai_financial_advisor`

---

## Collections & Schemas

### 1. `users`
- `_id`: ObjectId (Primary Key)
- `email`: String (Unique Index)
- `username`: String (Unique Index)
- `full_name`: String
- `hashed_password`: String (Bcrypt salted)
- `role`: String (`USER` / `ADMIN`)
- `monthly_income`: Number
- `risk_tolerance`: String (`CONSERVATIVE`, `MODERATE`, `AGGRESSIVE`)
- `is_active`: Boolean
- `created_at`: Date (Index)

### 2. `transactions`
- `_id`: ObjectId
- `user_id`: String (Index)
- `type`: String (`INCOME`, `EXPENSE`, `TRANSFER`, `INVESTMENT`)
- `category`: String (Index)
- `amount`: Number
- `currency`: String (`USD`)
- `description`: String (Text Index)
- `merchant`: String (Text Index)
- `date`: Date (Index)
- `payment_method`: String
- `location`: String
- `status`: String (`COMPLETED`)
- `is_anomaly`: Boolean
- `anomaly_score`: Number
- `created_at`: Date (Index)
- **Compound Index**: `{"user_id": 1, "date": -1}`

### 3. `budgets`
- `_id`: ObjectId
- `user_id`: String (Compound Index)
- `year`: Number (Compound Index)
- `month`: Number (Compound Index)
- `total_budget`: Number
- `category_limits`: Object

### 4. `financial_goals`
- `_id`: ObjectId
- `user_id`: String (Index)
- `name`: String
- `target_amount`: Number
- `current_amount`: Number
- `target_date`: Date
- `monthly_contribution`: Number
- `status`: String (`IN_PROGRESS`, `COMPLETED`)

### 5. `receipts`
- `_id`: ObjectId
- `user_id`: String (Index)
- `filename`: String
- `file_path`: String
- `parsed_data`: Object (Merchant, Items list, Subtotal, Tax, Total)
- `created_at`: Date

### 6. `fraud_alerts`
- `_id`: ObjectId
- `user_id`: String (Index)
- `transaction_id`: String
- `risk_level`: String (`LOW`, `MEDIUM`, `HIGH`)
- `risk_score`: Number
- `reasons`: Array of Strings
- `amount`: Number
- `merchant`: String
- `created_at`: Date

### 7. `portfolios`
- `_id`: ObjectId
- `user_id`: String (Index)
- `symbol`: String
- `name`: String
- `asset_type`: String (`Stock`, `ETF`, `Bond`, `Gold`)
- `quantity`: Number
- `purchase_price`: Number
- `current_price`: Number

### 8. `chat_history` & `audit_logs`
- `user_id`, `role`, `user_message`, `assistant_reply`, `action`, `endpoint`, `timestamp`

---

## Aggregation Pipelines

- **Cash Flow Aggregation**: Aggregates `$amount` grouped by `$type` for instant balance and savings computation.
- **Category Spend Aggregation**: Filters `$type: "EXPENSE"` and groups by `$category` sorted descending.
