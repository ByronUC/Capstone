import { Box, Container, Heading, Text, VStack, Input, Textarea, Button, SimpleGrid, Flex, Icon, Link } from "@chakra-ui/react"
import { FaMapMarkerAlt, FaPhone, FaEnvelope, FaClock, FaFacebook, FaInstagram, FaTiktok, FaWhatsapp, FaPaperPlane } from "react-icons/fa"
import { useInView } from "react-intersection-observer"
import { useState } from "react"
import emailjs from "@emailjs/browser"

export default function ContactSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    reason: "",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const SERVICE_ID = "service_rmrbv9d"
      const TEMPLATE_ID = "template_ggc6a06"
      const PUBLIC_KEY = "-FthNQ_3gPadpr5xn"

      await emailjs.send(
        SERVICE_ID,
        TEMPLATE_ID,
        {
          "contact-name": formData.name,
          "contact-email": formData.email,
          phone: formData.phone,
          reason: formData.reason,
        },
        PUBLIC_KEY
      )

      setMessage({ type: 'success', text: '¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.' })
      setFormData({ name: "", email: "", phone: "", reason: "" })
    } catch (error) {
      console.error("Error al enviar:", error)
      setMessage({ type: 'error', text: 'Hubo un problema al enviar el mensaje. Intenta nuevamente o contáctanos por WhatsApp.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box
      id="contact"
      py={{ base: 16, md: 24 }}
      bg="white"
      position="relative"
      ref={ref}
    >
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
              Contáctanos
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Estamos aquí para ayudarte
            </Text>
          </VStack>

          {/* Mapa de Google */}
          <Box
            w="full"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(20px)"}
            transition="all 0.8s 0.2s"
            borderRadius="2xl"
            overflow="hidden"
            boxShadow="xl"
            position="relative"
          >
            <Box
              as="iframe"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3329.30573282518!2d-70.65358142421181!3d-33.441340373393146!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9662c5a14e703231%3A0x20223c3a01387bc4!2sBombero%20Adolfo%20Ossa%201010%2C%208320327%20Santiago%2C%20Regi%C3%B3n%20Metropolitana!5e0!3m2!1ses-419!2scl!4v1755224959684!5m2!1ses-419!2scl"
              w="full"
              h={{ base: "300px", md: "450px" }}
              border="0"
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              title="Ubicación de Conectemos Chile"
            />
            <Box
              position="absolute"
              top={4}
              left={4}
              bg="white"
              p={4}
              borderRadius="xl"
              boxShadow="lg"
            >
              <VStack align="start" gap={2}>
                <Heading as="h3" fontSize="lg" color="gray.800">
                  <Icon as={FaMapMarkerAlt} color="#4285F4" mr={2} />
                  Nuestra Ubicación
                </Heading>
                <Text fontSize="sm" color="gray.700">
                  Bombero Adolfo Ossa 1010, Oficina 204, Santiago
                </Text>
                <Button
                  as={Link}
                  href="https://www.google.com/maps/dir//Bombero+Adolfo+Ossa+1010%2C+8320327+Santiago%2C+Regi%C3%B3n+Metropolitana/@-33.4413404,-70.6535814,17z/"
                  target="_blank"
                  size="sm"
                  bg="#4285F4"
                  color="white"
                  fontWeight="600"
                  borderRadius="full"
                  _hover={{ bg: "#3264C8" }}
                >
                  Cómo llegar
                </Button>
              </VStack>
            </Box>
          </Box>

          <SimpleGrid columns={{ base: 1, lg: 2 }} gap={12} w="full">
            {/* Información de contacto */}
            <VStack
              align="stretch"
              gap={6}
              opacity={inView ? 1 : 0}
              transform={inView ? "translateX(0)" : "translateX(-30px)"}
              transition="all 0.8s 0.3s"
            >
              <Box bg="white" p={6} borderRadius="xl" boxShadow="lg">
                <Flex gap={4} align="start">
                  <Icon as={FaMapMarkerAlt} fontSize="2xl" color="#4285F4" mt={1} />
                  <VStack align="start" gap={1}>
                    <Text fontWeight="700" fontSize="lg" color="gray.800">Dirección</Text>
                    <Text fontSize="md" color="gray.700">
                      Adolfo Bombero Ossa 1010, Oficina 204, Santiago
                    </Text>
                  </VStack>
                </Flex>
              </Box>

              <Box bg="white" p={6} borderRadius="xl" boxShadow="lg">
                <Flex gap={4} align="start">
                  <Icon as={FaPhone} fontSize="2xl" color="#4285F4" mt={1} />
                  <VStack align="start" gap={1}>
                    <Text fontWeight="700" fontSize="lg" color="gray.800">Teléfono</Text>
                    <Link href="tel:+56921991963" color="#4285F4" fontWeight="600">
                      +56 9 2199 1963
                    </Link>
                  </VStack>
                </Flex>
              </Box>

              <Box bg="white" p={6} borderRadius="xl" boxShadow="lg">
                <Flex gap={4} align="start">
                  <Icon as={FaEnvelope} fontSize="2xl" color="#4285F4" mt={1} />
                  <VStack align="start" gap={1}>
                    <Text fontWeight="700" fontSize="lg" color="gray.800">Email</Text>
                    <Link href="mailto:conectemoscl@gmail.com" color="#4285F4" fontWeight="600">
                      conectemoscl@gmail.com
                    </Link>
                  </VStack>
                </Flex>
              </Box>

              <Box bg="white" p={6} borderRadius="xl" boxShadow="lg">
                <Flex gap={4} align="start">
                  <Icon as={FaClock} fontSize="2xl" color="#4285F4" mt={1} />
                  <VStack align="start" gap={1}>
                    <Text fontWeight="700" fontSize="lg" color="gray.800">Horario de Atención</Text>
                    <Text fontSize="md" color="gray.700">
                      Lunes a Viernes: 9:00 - 20:00<br />
                      Sábados: 9:00 - 19:00<br />
                      Domingos: 9:00 - 14:00
                    </Text>
                  </VStack>
                </Flex>
              </Box>

              {/* Redes sociales */}
              <Flex gap={4} justify="center" pt={4}>
                <Link
                  href="https://www.instagram.com/conectemos.chile?igsh=MXNseDRxZGYyZGxwcA=="
                  target="_blank"
                  bg="rgba(66, 133, 244, 0.1)"
                  p={3}
                  borderRadius="full"
                  _hover={{ bg: "rgba(66, 133, 244, 0.2)", transform: "scale(1.1)" }}
                  transition="all 0.2s"
                >
                  <Icon as={FaInstagram} fontSize="2xl" color="#4285F4" />
                </Link>
                <Link
                  href="https://www.tiktok.com/@psicologo.ngel.da?_t=ZM-8zSsKIxiNRG&_r=1"
                  target="_blank"
                  bg="rgba(66, 133, 244, 0.1)"
                  p={3}
                  borderRadius="full"
                  _hover={{ bg: "rgba(66, 133, 244, 0.2)", transform: "scale(1.1)" }}
                  transition="all 0.2s"
                >
                  <Icon as={FaTiktok} fontSize="2xl" color="#4285F4" />
                </Link>
                <Link
                  href="https://wa.me/56921991963?text=Hola,%20me%20gustaría%20agendar%20una%20consulta%20en%20Conectemos%20Chile"
                  target="_blank"
                  bg="rgba(66, 133, 244, 0.1)"
                  p={3}
                  borderRadius="full"
                  _hover={{ bg: "rgba(66, 133, 244, 0.2)", transform: "scale(1.1)" }}
                  transition="all 0.2s"
                >
                  <Icon as={FaWhatsapp} fontSize="2xl" color="#4285F4" />
                </Link>
              </Flex>
            </VStack>

            {/* Formulario de contacto */}
            <Box
              as="form"
              onSubmit={handleSubmit}
              bg="white"
              p={{ base: 6, md: 8 }}
              borderRadius="2xl"
              boxShadow="xl"
              opacity={inView ? 1 : 0}
              transform={inView ? "translateX(0)" : "translateX(30px)"}
              transition="all 0.8s 0.4s"
            >
              <VStack gap={6}>
                {message && (
                  <Box
                    w="full"
                    p={4}
                    borderRadius="lg"
                    bg={message.type === 'success' ? 'green.50' : 'red.50'}
                    color={message.type === 'success' ? 'green.800' : 'red.800'}
                    border="1px solid"
                    borderColor={message.type === 'success' ? 'green.200' : 'red.200'}
                  >
                    {message.text}
                  </Box>
                )}

                <Box w="full">
                  <Text mb={2} fontWeight="600" fontSize="sm" color="gray.700">Nombre</Text>
                  <Input
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Tu nombre completo"
                    size="lg"
                    borderRadius="lg"
                    required
                  />
                </Box>

                <Box w="full">
                  <Text mb={2} fontWeight="600" fontSize="sm" color="gray.700">Correo electrónico</Text>
                  <Input
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="tu@email.com"
                    size="lg"
                    borderRadius="lg"
                    required
                  />
                </Box>

                <Box w="full">
                  <Text mb={2} fontWeight="600" fontSize="sm" color="gray.700">Celular</Text>
                  <Input
                    name="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="+56 9 1234 5678"
                    size="lg"
                    borderRadius="lg"
                    required
                  />
                </Box>

                <Box w="full">
                  <Text mb={2} fontWeight="600" fontSize="sm" color="gray.700">Motivo de consulta</Text>
                  <Textarea
                    name="reason"
                    value={formData.reason}
                    onChange={handleChange}
                    placeholder="Cuéntanos brevemente qué te trae a consultar con nosotros..."
                    rows={5}
                    size="lg"
                    borderRadius="lg"
                    required
                  />
                </Box>

                <Button
                  type="submit"
                  size="lg"
                  w="full"
                  bg="#E09600"
                  color="black"
                  fontWeight="700"
                  borderRadius="full"
                  leftIcon={<FaPaperPlane />}
                  _hover={{ bg: "#c98300", transform: "translateY(-2px)" }}
                  boxShadow="0 4px 20px rgba(224, 150, 0, 0.4)"
                  transition="all 0.25s"
                  isDisabled={loading}
                >
                  {loading ? "Enviando..." : "Contáctenme"}
                </Button>

                {/* Contacto rápido */}
                <VStack gap={3} w="full" pt={4} borderTop="1px solid" borderColor="gray.200">
                  <Text fontWeight="600" fontSize="md" color="gray.800">Contacto Rápido</Text>
                  <Text fontSize="sm" color="gray.600">También puedes contactarnos directamente:</Text>
                  <Flex gap={3} w="full">
                    <Button
                      as={Link}
                      href="https://wa.me/56921991963?text=Hola,%20me%20gustaría%20agendar%20una%20consulta%20en%20Conectemos%20Chile"
                      target="_blank"
                      flex={1}
                      bg="#25D366"
                      color="white"
                      leftIcon={<FaWhatsapp />}
                      _hover={{ bg: "#1DA851" }}
                    >
                      WhatsApp
                    </Button>
                    <Button
                      as={Link}
                      href="tel:+56921991963"
                      flex={1}
                      bg="rgba(66, 133, 244, 0.1)"
                      color="#1a56db"
                      leftIcon={<FaPhone />}
                      _hover={{ bg: "rgba(66, 133, 244, 0.2)" }}
                    >
                      Llamar
                    </Button>
                  </Flex>
                </VStack>
              </VStack>
            </Box>
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
