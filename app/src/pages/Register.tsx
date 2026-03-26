import RegisterForm from '@/components/auth/RegisterForm';

const Register = () => {
  return (
    <div className="min-h-screen flex items-center justify-center py-20 px-4 bg-gradient-to-br from-sage-50 via-white to-lavender-50">
      {/* Decorative Elements */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-sage-200/20 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-lavender-200/20 rounded-full blur-3xl" />
      
      <div className="relative w-full max-w-md">
        <RegisterForm />
      </div>
    </div>
  );
};

export default Register;
