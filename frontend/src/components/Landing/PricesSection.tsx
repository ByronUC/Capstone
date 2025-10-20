import { Box, Container, Heading, Text, VStack, SimpleGrid, Button, List, Icon, Badge } from "@chakra-ui/react"
import { FaCalendarAlt, FaCheckCircle, FaInfoCircle } from "react-icons/fa"
import { useInView } from "react-intersection-observer"

export default function PricesSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  const handleNavClick = (href: string) => {
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  const prices = [
    {
      name: "Terapia Individual",
      price: "$30.500",
      cycle: "Por sesión",
      features: [
        "Sesión de 45-50 minutos",
        "Atención personalizada",
        "Posibilidad de sesión online o presencial",
        "Seguimiento continuo del paciente",
        "Boleta reembolsable con Isapre y/o seguro complementario",
        "Horarios flexibles",
        "Evaluación inicial completa"
      ],
      featured: false
    },
    {
      name: "Plan Mensual",
      price: "$110.000",
      cycle: "4 sesiones / mes",
      features: [
        "Sesiones semanales de 45-50 minutos",
        "Ahorro de $12.000 respecto a sesiones individuales",
        "Atención personalizada",
        "Seguimiento continuo del paciente",
        "Envío de material complementario",
        "Posibilidad de sesión online o presencial",
        "Flexibilidad para cambio de horarios",
        "Boleta reembolsable con Isapre y/o seguro complementario"
      ],
      featured: true
    },
    {
      name: "Terapia de Parejas",
      price: "$38.750",
      cycle: "Por sesión",
      features: [
        "Sesión de 45-50 minutos",
        "Sesión extendida de 2 horas por solo $45.000",
        "Atención personalizada para ambos miembros",
        "Posibilidad de sesión online o presencial",
        "Seguimiento continuo de la pareja",
        "Herramientas de comunicación efectiva",
        "Material de apoyo personalizado",
        "Boleta reembolsable con Isapre y/o seguro complementario"
      ],
      featured: false
    }
  ]

  return (
    <Box
      id="prices"
      py={{ base: 16, md: 24 }}
      bg="gray.50"
      position="relative"
      ref={ref}
    >
      {/* Decorative elements */}
      <Box position="absolute" top="10%" left="5%" w="200px" h="200px" borderRadius="50%" bg="rgba(66, 133, 244, 0.05)" />

      <Container maxW="1280px">
        <VStack gap={12}>
          <VStack
            gap={4}
            textAlign="center"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.6s"
          >
            <Heading
              as="h2"
              fontSize={{ base: "3xl", md: "4xl", lg: "5xl" }}
              fontWeight="700"
              color="gray.800"
            >
              Nuestros Precios
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Inversión en tu bienestar emocional
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, lg: 3 }} gap={8} w="full">
            {prices.map((plan, index) => (
              <Box
                key={index}
                bg="white"
                borderRadius="2xl"
                overflow="hidden"
                boxShadow={plan.featured ? "2xl" : "lg"}
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(30px)"}
                transition={`all 0.8s ${0.2 + index * 0.1}s`}
                position="relative"
                borderWidth={plan.featured ? "2px" : "0"}
                borderColor={plan.featured ? "#4285F4" : "transparent"}
                _hover={{ transform: "translateY(-8px)", boxShadow: "2xl" }}
              >
                {plan.featured && (
                  <Badge
                    position="absolute"
                    top={4}
                    right={4}
                    colorScheme="blue"
                    fontSize="sm"
                    px={4}
                    py={2}
                    borderRadius="full"
                  >
                    Recomendado
                  </Badge>
                )}

                <VStack align="stretch" p={8} gap={6}>
                  <VStack align="center" gap={2}>
                    <Heading as="h3" fontSize="2xl" color="gray.800">
                      {plan.name}
                    </Heading>
                    <Text fontSize="4xl" fontWeight="bold" color="#4285F4">
                      {plan.price}
                    </Text>
                    <Text fontSize="md" color="gray.600">
                      {plan.cycle}
                    </Text>
                  </VStack>

                  <List.Root as="ul" gap={3}>
                    {plan.features.map((feature, idx) => (
                      <List.Item key={idx} display="flex" alignItems="start" gap={2}>
                        <List.Indicator asChild color="#4CAF50">
                          <Icon fontSize="lg" mt={0.5}>
                            <FaCheckCircle />
                          </Icon>
                        </List.Indicator>
                        <Text fontSize="sm" color="gray.700" lineHeight="1.6">
                          {feature}
                        </Text>
                      </List.Item>
                    ))}
                  </List.Root>

                  <Button
                    mt={4}
                    bg={plan.featured ? "#E09600" : "rgba(66, 133, 244, 0.1)"}
                    color={plan.featured ? "black" : "#1a56db"}
                    fontWeight="700"
                    borderRadius="full"
                    leftIcon={plan.featured ? <FaCheckCircle /> : <FaCalendarAlt />}
                    _hover={{ bg: plan.featured ? "#c98300" : "rgba(66, 133, 244, 0.2)" }}
                    onClick={() => handleNavClick("#booking")}
                    size="lg"
                  >
                    {plan.featured ? "Elegir Este Plan" : "Agendar Ahora"}
                  </Button>
                </VStack>
              </Box>
            ))}
          </SimpleGrid>

          <Box
            bg="blue.50"
            p={6}
            borderRadius="xl"
            display="flex"
            alignItems="center"
            gap={3}
            opacity={inView ? 1 : 0}
            transition="all 0.8s 0.5s"
          >
            <Icon as={FaInfoCircle} fontSize="2xl" color="#4285F4" />
            <Text fontSize="md" color="gray.700">
              Todos los planes incluyen boletas reembolsables con Isapre y seguros complementarios.
            </Text>
          </Box>
        </VStack>
      </Container>
    </Box>
  )
}
