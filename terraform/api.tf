resource "aws_apigatewayv2_integration" "qr_service_integration" {
  api_id             = local.api_gateway_id
  integration_type   = "AWS_PROXY"
  integration_uri    = module.qr-service.lambda_function_arn
  integration_method = "ANY"
  passthrough_behavior = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_route" "qr_service_route" {
  api_id    = local.api_gateway_id
  route_key = "POST /v1/notion/qr"
  target    = "integrations/${aws_apigatewayv2_integration.qr_service_integration.id}"
}

resource "aws_lambda_permission" "qr_service_api_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.qr-service.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${local.execution_arn}/*"
}