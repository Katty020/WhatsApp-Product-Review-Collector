type Review = {
  id: string;
  contact_number: string;
  user_name: string;
  product_name: string;
  product_review: string;
  created_at: string;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function fetchReviews(): Promise<Review[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/reviews`, {
      next: { revalidate: 5 },
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      console.error("Failed to load reviews", response.statusText);
      return [];
    }

    return response.json();
  } catch (error) {
    console.error("Failed to load reviews", error);
    return [];
  }
}

const dateFormatter = new Intl.DateTimeFormat(undefined, {
  dateStyle: "medium",
  timeStyle: "short",
});

export default async function Home() {
  const reviews = await fetchReviews();
  const fallbackReview: Review = {
    id: "placeholder",
    contact_number: "whatsapp:+919755501001",
    user_name: "Aditi",
    product_name: "Samsung Galaxy",
    product_review: "Amazing battery life, very satisfied.",
    created_at: new Date().toISOString(),
  };
  const reviewsToDisplay = reviews.length > 0 ? reviews : [fallbackReview];

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">WhatsApp Product Review Collector</p>
          <h1>See what customers are saying</h1>
          <p className="subtitle">
            Reviews sent by WhatsApp via the Twilio sandbox appear here as soon
            as they are saved in Postgres.
          </p>
        </div>
      </header>

      <section className="card">
        <div className="card-header">
          <div>
            <h2>Latest reviews</h2>
            <p>
              Showing{" "}
              {reviews.length > 0 ? reviews.length : "a sample"} submission
            </p>
          </div>
          <span className="pill">Live</span>
        </div>

        <div className="table">
          <div className="table-head">
            <span>Customer</span>
            <span>Product</span>
            <span>Review</span>
            <span>Received</span>
          </div>
          {reviewsToDisplay.map((review) => (
            <div key={review.id} className="table-row">
              <div>
                <p className="title">{review.user_name}</p>
                <p className="muted">{review.contact_number}</p>
              </div>
              <p className="title">{review.product_name}</p>
              <p>{review.product_review}</p>
              <p className="muted">
                {dateFormatter.format(new Date(review.created_at))}
              </p>
            </div>
          ))}
        </div>
        {reviews.length === 0 && (
          <p>
            Send a review over WhatsApp!
          </p>
        )}
      </section>
    </div>
  );
}
