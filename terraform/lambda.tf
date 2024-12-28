module "qr-service" {
  source = "terraform-aws-modules/lambda/aws"

  function_name      = var.lambda_function_name
  description        = "Generates QR codes for Notion integration and updates fields via webhook."
  handler            = "qr_service.lambda_handler"
  runtime            = "python3.12"
  source_path        = "../lambda/src"
  attach_policy_json = true

  policy_json = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      # Permission to read/write S3 for QR code files
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = "arn:aws:s3:::${var.s3_bucket}/*"
      },
      # Log permissions
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })

  environment_variables = {
    BUCKET_NAME = var.s3_bucket
  }

  tags = {
    project = local.project_name
  }
}