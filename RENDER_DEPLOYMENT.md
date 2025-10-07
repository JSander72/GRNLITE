# Render.com Deployment Guide

## Prerequisites for Render Deployment

### 1. Environment Variables Setup

You **MUST** set these environment variables in your Render dashboard before deployment:

#### **Main Django Service (GRNLITE)**
```
JWT_SECRET=<generate-with-openssl-rand-base64-32>
JWT_REFRESH_SECRET=<generate-with-openssl-rand-base64-32>
DJANGO_SECRET_KEY=<generate-with-django-secret-key-generator>
```

#### **Keep-Alive Service (GRNLITE-KeepAlive)**
No additional environment variables needed - uses values from render.yaml.

### 2. Generate Secure Secrets

```bash
# Generate JWT secrets
openssl rand -base64 32
openssl rand -base64 32

# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment Steps

### 1. **Update Environment Variables in Render Dashboard**

1. Go to your Render dashboard
2. Select your **GRNLITE** service
3. Navigate to **Environment** tab
4. Add these environment variables:
   - `JWT_SECRET`: [generated secret]
   - `JWT_REFRESH_SECRET`: [generated secret] 
   - `DJANGO_SECRET_KEY`: [generated secret]

### 2. **Verify render.yaml Configuration**

The `render.yaml` file should include these environment variables:
```yaml
envVars:
  - key: JWT_SECRET
    sync: false
  - key: JWT_REFRESH_SECRET
    sync: false
  - key: DJANGO_SECRET_KEY
    sync: false
```

### 3. **Deploy**

1. Push your changes to GitHub
2. Render will automatically detect changes and redeploy
3. Monitor the build logs for any errors

## Verification Checklist

After deployment, verify:

- [ ] Django service starts without errors
- [ ] Keep-alive service starts and makes requests
- [ ] JWT authentication works
- [ ] Database connections are successful
- [ ] Static files are served correctly

## Troubleshooting

### **Build Fails with "Environment variable must be set"**
- Ensure all required environment variables are set in Render dashboard
- Check that variable names match exactly (case-sensitive)

### **JWT Errors in Production**
- Verify JWT_SECRET and JWT_REFRESH_SECRET are set correctly
- Ensure secrets are base64 encoded and sufficient length

### **Django Secret Key Errors**
- Verify DJANGO_SECRET_KEY is set
- Ensure it's a proper Django secret key format

### **Keep-Alive Service Not Working**
- Check that RENDER_EXTERNAL_URL points to your main app
- Verify health endpoint is accessible
- Monitor keep-alive service logs

## Development vs Production

### **Development (Local)**
- Environment variables are optional (defaults provided)
- Uses development secrets (insecure)
- Keep-alive service disabled
- Debug mode enabled

### **Production (Render)**
- Environment variables required
- Must use secure, generated secrets
- Keep-alive service enabled
- Debug mode disabled

## Security Notes

1. **Never commit secrets to version control**
2. **Generate unique secrets for production**
3. **Use Render's environment variable sync: false for secrets**
4. **Regularly rotate secrets in production**

## Support

If deployment fails:
1. Check Render build logs
2. Verify all environment variables are set
3. Ensure render.yaml syntax is correct
4. Contact support with specific error messages