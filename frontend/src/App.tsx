mport { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { CustomizationProvider } from './contexts/CustomizationContext';
import { PrivateRoute } from './components/layout/PrivateRoute';
import { Header } from './components/layout/Header';
import { LoginPage } from './pages/LoginPage';
import { HomePage } from './pages/HomePage';
function App() {
  return (
    <AuthProvider>
      <CustomizationProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <>
                    <Header />
                    <HomePage />
                  </>
                </PrivateRoute>
              }
            />
          </Routes>
        </BrowserRouter>
      </CustomizationProvider>
    </AuthProvider>
  );
}
export default App;