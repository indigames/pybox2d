from math import sqrt
import sys

from .framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2FixtureDef, b2PolygonShape, b2Random,
                   b2Vec2, b2_epsilon, b2BodyDef, b2ChainShape, b2ParticleGroupDef, b2ParticleColor)

k_ParticleColors = (
    b2ParticleColor(0xff, 0x00, 0x00, 0xff),  # red
    b2ParticleColor(0x00, 0xff, 0x00, 0xff),  # green
    b2ParticleColor(0x00, 0x00, 0xff, 0xff),  # blue
    b2ParticleColor(0xff, 0x8c, 0x00, 0xff),  # orange
    b2ParticleColor(0x00, 0xce, 0xd1, 0xff),  # turquoise
    b2ParticleColor(0xff, 0x00, 0xff, 0xff),  # magenta
    b2ParticleColor(0xff, 0xd7, 0x00, 0xff),  # gold
    b2ParticleColor(0x00, 0xff, 0xff, 0xff),  # cyan
)
k_ParticleColorsCount = 8


class Impulse (Framework):
    name = "Impulse Test"
    description = ''

    m_linear = False

    def __init__(self):
        super(Impulse, self).__init__()

        self.kBoxLeft = -4
        self.kBoxRight = 4
        self.kBoxBottom = 0
        self.kBoxTop = 8

        bd = b2BodyDef()
        ground = self.world.CreateBody(bd)

        box = [b2Vec2(self.kBoxLeft, self.kBoxBottom),
            b2Vec2(self.kBoxRight, self.kBoxBottom),
            b2Vec2(self.kBoxRight, self.kBoxTop),
            b2Vec2(self.kBoxLeft, self.kBoxTop)]
        
        shape = b2ChainShape()
        shape.CreateLoop(box)

        ground.CreateFixture(b2FixtureDef(shape=shape, density=0.0))

        self.particleSystem.SetRadius(0.05)
        self.particleSystem.SetDamping(0.2)

        shape = b2PolygonShape()
        shape.SetAsBox(2, 2, b2Vec2(0, 2.01), 0)
        pd = b2ParticleGroupDef()
        pd.flags = 1 << 5
        # pd.flags = TestMain::GetParticleParameterValue();
        pd.shape = shape
        pd.color = b2ParticleColor(255, 0, 0, 255)
        group = self.particleSystem.CreateParticleGroup(pd)
        # if pd.flags & b2_colorMixingParticle:
            # self.ColorParticleGroup(group, 0)

    def ColorParticleGroup(self, group, particlesPerColor):
        colorBuffer = self.particleSystem.GetColorBuffer()
        particleCount = group.GetParticleCount()
        groupStart = group.GetBufferIndex()
        groupEnd = particleCount + groupStart
        colorCount = k_ParticleColorsCount
        if particlesPerColor == 0:
            particlesPerColor = particleCount / colorCount
            if particlesPerColor == 0:
                particlesPerColor = 1

        for i in range(groupStart, groupEnd):
            colorBuffer[i] = k_ParticleColors[round(i / particlesPerColor)]

    def ApplyImpulseOrForce(self, direction):
        particleSystem = self.world.GetParticleSystemList()
        particleGroup = particleSystem.GetParticleGroupList()
        numParticles = particleGroup.GetParticleCount()

        if self.m_linear:
            kImpulseMagnitude = 0.005
            impulse = kImpulseMagnitude * direction * numParticles
            particleGroup.ApplyLinearImpulse(impulse)
        else:
            kForceMagnitude = 1.0
            force = kForceMagnitude * direction * numParticles
            particleGroup.ApplyForce(force)

    def Step(self, settings):
        super(Impulse, self).Step(settings)

    def MouseUp(self, p):
        super().MouseUp(p)
        isInsideBox = self.kBoxLeft <= p.x and p.x <= self.kBoxRight and self.kBoxBottom <= p.y and p.y <= self.kBoxTop
        if isInsideBox:
            kBoxCenter = b2Vec2(
                0.5 * (self.kBoxLeft + self.kBoxRight), 0.5 * (self.kBoxBottom + self.kBoxTop))
            direction = p - kBoxCenter
            direction.Normalize()
            self.ApplyImpulseOrForce(direction)

    def Keyboard(self, key):
        if key == Keys.K_l:
            self.m_linear = True
        if key == Keys.K_f:
            self.m_linear = False


if __name__ == "__main__":
    main(Impulse)
