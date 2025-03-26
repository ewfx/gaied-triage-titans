import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  CircularProgress,
  Box,
  Alert,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import WarningIcon from "@mui/icons-material/Warning";

interface Ticket {
  email: string;
  request_type: string;
  confidence_score: number;
  reasoning: string;
  is_duplicate: boolean;
  download_url: string;
}

const Dashboard: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/classify_emails")
      .then((response) => {
        setTickets(response.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load tickets.");
        setLoading(false);
      });
  }, []);

  if (loading)
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  if (error)
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );

  return (
    <Box p={4} sx={{ backgroundColor: "#f5f5f5", minHeight: "100vh" }}>
      <Typography variant="h4" fontWeight="bold" textAlign="center" mb={4}>
        📌 Ticket Dashboard
      </Typography>
      <Grid container spacing={3}>
        {tickets.map((ticket, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
            <Card
              sx={{
                boxShadow: 3,
                borderRadius: 2,
                border: ticket.is_duplicate ? "2px solid red" : "none",
              }}
            >
              <CardContent>
                <Typography
                  variant="h6"
                  fontWeight="bold"
                  color="primary"
                  gutterBottom
                >
                  {ticket.request_type}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  <strong>Email:</strong> {ticket.email}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  <strong>Confidence:</strong> {ticket.confidence_score * 100}%
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  <strong>Reasoning:</strong> {ticket.reasoning}
                </Typography>

                {ticket.is_duplicate && (
                  <Box display="flex" alignItems="center" color="error.main" mt={1}>
                    <WarningIcon fontSize="small" />
                    <Typography variant="body2" ml={1}>
                      Duplicate Email Detected
                    </Typography>
                  </Box>
                )}

                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<DownloadIcon />}
                  href={ticket.download_url}
                  target="_blank"
                  fullWidth
                  sx={{ mt: 2 }}
                >
                  Download PDF
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Dashboard;
